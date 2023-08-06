# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
#
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals
from builtins import str
import six

import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.utils import timezone

from lino import mixins
from lino.api import dd, rt, _, pgettext

from .choicelists import (
    DurationUnits, Recurrencies, Weekdays, AccessClasses)
from .utils import setkw, dt2kw, when_text

from lino.modlib.plausibility.choicelists import Checker
from lino.modlib.printing.mixins import TypedPrintable
from lino.modlib.users.mixins import UserAuthored, Assignable
from lino_xl.lib.postings.mixins import Postable
from lino_xl.lib.outbox.mixins import MailableType, Mailable
from lino_xl.lib.contacts.mixins import ContactRelated
from lino.modlib.office.roles import OfficeStaff
from .workflows import (TaskStates, EntryStates, GuestStates)

# removed from default config because you cannot easily unload it again
# from .workflows import take

from .mixins import Component
from .mixins import EventGenerator, RecurrenceSet, Reservation
from .mixins import Ended
from .mixins import MoveEntryNext, UpdateEntries, UpdateEntriesByEvent
from .actions import ShowEntriesByDay

from .ui import ConflictingEvents

DEMO_START_YEAR = 2013


class CalendarType(object):

    def validate_calendar(self, cal):
        pass


class LocalCalendar(CalendarType):
    label = "Local Calendar"


class GoogleCalendar(CalendarType):
    label = "Google Calendar"

    def validate_calendar(self, cal):
        if not cal.url_template:
            cal.url_template = \
                "https://%(username)s:%(password)s@www.google.com/calendar/dav/%(username)s/"

CALENDAR_CHOICES = []
CALENDAR_DICT = {}


def register_calendartype(name, instance):
    CALENDAR_DICT[name] = instance
    CALENDAR_CHOICES.append((name, instance.label))

register_calendartype('local', LocalCalendar())
register_calendartype('google', GoogleCalendar())


class RemoteCalendar(mixins.Sequenced):

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'RemoteCalendar')
        verbose_name = _("Remote Calendar")
        verbose_name_plural = _("Remote Calendars")
        ordering = ['seqno']

    type = models.CharField(_("Type"), max_length=20,
                            default='local',
                            choices=CALENDAR_CHOICES)
    url_template = models.CharField(_("URL template"),
                                    max_length=200, blank=True)  # ,null=True)
    username = models.CharField(_("Username"),
                                max_length=200, blank=True)  # ,null=True)
    password = dd.PasswordField(_("Password"),
                                max_length=200, blank=True)  # ,null=True)
    readonly = models.BooleanField(_("read-only"), default=False)

    def get_url(self):
        if self.url_template:
            return self.url_template % dict(
                username=self.username,
                password=self.password)
        return ''

    def save(self, *args, **kw):
        ct = CALENDAR_DICT.get(self.type)
        ct.validate_calendar(self)
        super(RemoteCalendar, self).save(*args, **kw)


class Room(mixins.BabelNamed, ContactRelated):
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Room')
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    description = dd.RichTextField(_("Description"), blank=True)

dd.update_field(
    Room, 'company', verbose_name=_("Responsible"))    
dd.update_field(
    Room, 'contact_person', verbose_name=_("Contact person"))    

class Priority(mixins.BabelNamed):
    class Meta:
        app_label = 'cal'
        verbose_name = _("Priority")
        verbose_name_plural = _('Priorities')
    ref = models.CharField(max_length=1)


@dd.python_2_unicode_compatible
class EventType(mixins.BabelNamed, mixins.Sequenced, MailableType):
    templates_group = 'cal/Event'

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'EventType')
        verbose_name = _("Calendar entry type")
        verbose_name_plural = _("Calendar entry types")
        ordering = ['seqno']

    description = dd.RichTextField(
        _("Description"), blank=True, format='html')
    is_appointment = models.BooleanField(_("Appointment"), default=True)
    all_rooms = models.BooleanField(_("Locks all rooms"), default=False)
    locks_user = models.BooleanField(_("Locks the user"), default=False)

    start_date = models.DateField(
        verbose_name=_("Start date"),
        blank=True, null=True)
    event_label = dd.BabelCharField(
        _("Entry label"), max_length=200, blank=True)
    # , default=_("Calendar entry"))
    # default values for a Babelfield don't work as expected

    max_conflicting = models.PositiveIntegerField(
        _("Simultaneous entries"), default=1)
    max_days = models.PositiveIntegerField(
        _("Maximum days"), default=1)

    def __str__(self):
        # when selecting an Event.event_type it is more natural to
        # have the event_label. It seems that the current `name` field
        # is actually never used.
        return settings.SITE.babelattr(self, 'event_label') \
            or settings.SITE.babelattr(self, 'name')


class GuestRole(mixins.BabelNamed):
    templates_group = 'cal/Guest'

    class Meta:
        app_label = 'cal'
        verbose_name = _("Guest Role")
        verbose_name_plural = _("Guest Roles")


def default_color():
    d = Calendar.objects.all().aggregate(models.Max('color'))
    n = d['color__max'] or 0
    return n + 1


class Calendar(mixins.BabelNamed):

    COLOR_CHOICES = [i + 1 for i in range(32)]

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Calendar')
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")

    description = dd.RichTextField(_("Description"), blank=True, format='html')

    color = models.IntegerField(
        _("color"), default=default_color,
        validators=[MinValueValidator(1), MaxValueValidator(32)]
    )
    # choices=COLOR_CHOICES)


class Subscription(UserAuthored):

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Subscription')
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        unique_together = ['user', 'calendar']

    manager_roles_required = dd.login_required(OfficeStaff)

    calendar = dd.ForeignKey(
        'cal.Calendar', help_text=_("The calendar you want to subscribe to."))

    is_hidden = models.BooleanField(
        _("hidden"), default=False,
        help_text=_("""Whether this subscription should "
        "initially be displayed as a hidden calendar."""))


class Task(Component):
    class Meta:
        app_label = 'cal'
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        abstract = dd.is_abstract_model(__name__, 'Task')

    due_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Due date"))
    due_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Due time"))
    # ~ done = models.BooleanField(_("Done"),default=False) # iCal:COMPLETED
    # iCal:PERCENT
    percent = models.IntegerField(_("Duration value"), null=True, blank=True)
    state = TaskStates.field(
        default=TaskStates.todo.as_callable)  # iCal:STATUS

    # def before_ui_save(self, ar, **kw):
    #     if self.state == TaskStates.todo:
    #         self.state = TaskStates.started
    #     return super(Task, self).before_ui_save(ar, **kw)

    # def on_user_change(self,request):
        # if not self.state:
            # self.state = TaskState.todo
        # self.user_modified = True

    def is_user_modified(self):
        return self.state != TaskStates.todo

    @classmethod
    def on_analyze(cls, lino):
        # lino.TASK_AUTO_FIELDS = dd.fields_list(cls,
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(
            cls, """start_date start_time summary""")
        super(Task, cls).on_analyze(lino)

    # def __unicode__(self):
        # ~ return "#" + str(self.pk)

class EventPolicy(mixins.BabelNamed, RecurrenceSet):
    class Meta:
        app_label = 'cal'
        verbose_name = _("Recurrency policy")
        verbose_name_plural = _('Recurrency policies')
        abstract = dd.is_abstract_model(__name__, 'EventPolicy')

    event_type = dd.ForeignKey(
        'cal.EventType', null=True, blank=True)



class RecurrentEvent(mixins.BabelNamed, RecurrenceSet, EventGenerator,
                     UserAuthored):
    class Meta:
        app_label = 'cal'
        verbose_name = _("Recurring event")
        verbose_name_plural = _("Recurring events")
        abstract = dd.is_abstract_model(__name__, 'RecurrentEvent')

    event_type = models.ForeignKey('cal.EventType', blank=True, null=True)
    description = dd.RichTextField(
        _("Description"), blank=True, format='html')

    def before_auto_event_save(self, obj):
        if self.end_date:  # and self.end_date != self.start_date:
            duration = self.end_date - self.start_date
            obj.end_date = obj.start_date + duration
        super(RecurrentEvent, self).before_auto_event_save(obj)

    # def on_create(self,ar):
        # super(RecurrentEvent,self).on_create(ar)
        # self.event_type = settings.SITE.site_config.holiday_event_type

    # def __unicode__(self):
        # return self.summary

    def update_cal_rset(self):
        return self

    def update_cal_from(self, ar):
        return self.start_date

    def update_cal_event_type(self):
        return self.event_type

    def update_cal_summary(self, et, i):
        return six.text_type(self)

    def care_about_conflicts(self, we):
        """Recurrent events don't care about conflicts. A holiday won't move
        just because some other event has been created before on that date.

        """
        return False

dd.update_field(
    RecurrentEvent, 'every_unit',
    default=Recurrencies.yearly.as_callable, blank=False, null=False)


class UpdateGuests(dd.MultipleRowAction):

    label = _('Update Guests')
    # icon_name = 'lightning'
    button_text = ' ☷ '  # 2637

    def run_on_row(self, obj, ar):
        if settings.SITE.loading_from_dump:
            return 0
        if not obj.state.edit_guests:
            ar.info("not state.edit_guests")
            return 0
        # existing = set([g.partner.pk for g in obj.guest_set.all()])
        existing = {g.partner.pk : g for g in obj.guest_set.all()}
        n = 0
        for sg in obj.suggest_guests():
            eg = existing.pop(sg.partner.pk, None)
            if eg is None:
                sg.save()
                n += 1
        # remove unwanted participants
        for pk, g in existing.items():
            if g.state == GuestStates.invited:
                g.delete()
        return n


class ExtAllDayField(dd.VirtualField):

    """
    An editable virtual field needed for
    communication with the Ext.ensible CalendarPanel
    because we consider the "all day" checkbox
    equivalent to "empty start and end time fields".
    """

    editable = True

    def __init__(self, *args, **kw):
        dd.VirtualField.__init__(self, models.BooleanField(*args, **kw), None)

    def set_value_in_object(self, request, obj, value):
        if value:
            obj.end_time = None
            obj.start_time = None
        else:
            if not obj.start_time:
                obj.start_time = datetime.time(9, 0, 0)
            if not obj.end_time:
                pass
                # obj.end_time = datetime.time(10, 0, 0)
        # obj.save()

    def value_from_object(self, obj, ar):
        # logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        return (obj.start_time is None)


@dd.python_2_unicode_compatible
class Event(Component, Ended, Assignable, TypedPrintable, Mailable, Postable):
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Event')
        # abstract = True
        verbose_name = _("Calendar entry")
        verbose_name_plural = _("Calendar entries")
        # verbose_name = pgettext("cal", "Event")
        # verbose_name_plural = pgettext("cal", "Events")

    update_guests = UpdateGuests()
    update_events = UpdateEntriesByEvent()
    show_today = ShowEntriesByDay('start_date')

    event_type = models.ForeignKey('cal.EventType', blank=True, null=True)

    transparent = models.BooleanField(_("Transparent"), default=False)
    room = dd.ForeignKey('cal.Room', null=True, blank=True)
    priority = models.ForeignKey(Priority, null=True, blank=True)
    state = EntryStates.field(
        default=EntryStates.suggested.as_callable)
    all_day = ExtAllDayField(_("all day"))

    move_next = MoveEntryNext()

    show_conflicting = dd.ShowSlaveTable(ConflictingEvents)

    def strftime(self):
        if not self.start_date:
            return ''
        d = self.start_date.strftime(settings.SITE.date_format_strftime)
        if self.start_time:
            t = self.start_time.strftime(
                settings.SITE.time_format_strftime)
            return "%s %s" % (d, t)
        else:
            return d

    def __str__(self):
        if self.summary:
            s = self.summary
        elif self.event_type:
            s = str(self.event_type)
        elif self.pk:
            s = self._meta.verbose_name + " #" + str(self.pk)
        else:
            s = _("Unsaved %s") % self._meta.verbose_name
        when = self.strftime()
        if when:
            s = "{} ({})".format(s, when)
        return s

    def get_change_observers(self):
        # implements ChangeObservable
        if not self.is_user_modified():
            return
        for x in super(Event, self).get_change_observers():
            yield x
        for u in (self.user, self.assigned_to):
            if u is not None:
                yield (u, u.mail_mode)
    
        
    def has_conflicting_events(self):
        """Whether this event has any conflicting events.
        
        This is roughly equivalent to asking whether
        :meth:`get_conflicting_events()` returns more than 0 events.

        Except when this event's type tolerates more than one events
        at the same time.

        """
        qs = self.get_conflicting_events()
        if qs is None:
            return False
        if self.event_type is not None:
            if qs.filter(event_type__all_rooms=True).count() > 0:
                return True
            n = self.event_type.max_conflicting - 1
        else:
            n = 0
        return qs.count() > n

    def get_conflicting_events(self):
        """
        Return a QuerySet of Events that conflict with this one.
        Must work also when called on an unsaved instance.
        May return None to indicate an empty queryset.
        Applications may override this to add specific conditions.
        """
        if self.transparent:
            return
        if self.state.transparent:
            return
        # return False
        # Event = dd.resolve_model('cal.Event')
        # ot = ContentType.objects.get_for_model(RecurrentEvent)
        qs = self.__class__.objects.filter(transparent=False)
        end_date = self.end_date or self.start_date
        flt = Q(start_date=self.start_date, end_date__isnull=True)
        flt |= Q(end_date__isnull=False,
                 start_date__lte=self.start_date, end_date__gte=end_date)
        if end_date == self.start_date:
            if self.start_time and self.end_time:
                # the other starts before me and ends after i started
                c1 = Q(start_time__lte=self.start_time,
                       end_time__gt=self.start_time)
                # the other ends after me and started before i ended
                c2 = Q(end_time__gte=self.end_time,
                       start_time__lt=self.end_time)
                # the other is full day
                c3 = Q(end_time__isnull=True, start_time__isnull=True)
                flt &= (c1 | c2 | c3)
        qs = qs.filter(flt)

        # saved events don't conflict with themselves:
        if self.id is not None:
            qs = qs.exclude(id=self.id)

        # automatic events never conflict with other generated events
        # of same owner. Rule needed for update_events.
        if self.auto_type:
            qs = qs.exclude(
                # auto_type=self.auto_type,
                auto_type__isnull=False,
                owner_id=self.owner_id, owner_type=self.owner_type)

        # transparent events (cancelled or omitted) usually don't
        # cause a conflict with other events (e.g. a holiday), except
        # if the other event has the same owner (because a cancelled
        # course lesson should not tolerate another lesson on the same
        # date).
        qs = qs.filter(
            Q(state__in=EntryStates.filter(transparent=False)) | Q(
                owner_id=self.owner_id, owner_type=self.owner_type))

        if self.room is None:
            # a non-holiday event without room conflicts with a
            # holiday event
            if self.event_type is None or not self.event_type.all_rooms:
                qs = qs.filter(event_type__all_rooms=True)
        else:
            # other event in the same room
            c1 = Q(room=self.room)
            # other event locks all rooms (e.g. holidays)
            # c2 = Q(room__isnull=False, event_type__all_rooms=True)
            c2 = Q(event_type__all_rooms=True)
            qs = qs.filter(c1 | c2)
        if self.user is not None:
            if self.event_type is not None:
                if self.event_type.locks_user:
                    # c1 = Q(event_type__locks_user=False)
                    # c2 = Q(user=self.user)
                    # qs = qs.filter(c1|c2)
                    qs = qs.filter(user=self.user, event_type__locks_user=True)
        # qs = Event.objects.filter(flt,owner_type=ot)
        # if we.start_date.month == 7:
            # print 20131011, self, we.start_date, qs.count()
        # print 20131025, qs.query
        return qs

    def is_fixed_state(self):
        return self.state.fixed
        # return self.state in EntryStates.editable_states

    def is_user_modified(self):
        return self.state != EntryStates.suggested

    def after_ui_save(self, ar, cw):
        super(Event, self).after_ui_save(ar, cw)
        self.update_guests.run_from_code(ar)

    def suggest_guests(self):
        """Yield the list of Guest instances to be added to this Event.  This
        method is called from :meth:`update_guests`.

        """
        if self.owner:
            for obj in self.owner.suggest_cal_guests(self):
                yield obj

    def get_event_summary(event, ar):
        """How this event should be summarized in contexts where possibly
        another user is looking (i.e. currently in invitations of
        guests, or in the extensible calendar panel).

        """
        # from django.utils.translation import ugettext as _
        s = event.summary
        # if event.owner_id:
        #     s += " ({0})".format(event.owner)
        if event.user is not None and event.user != ar.get_user():
            if event.access_class == AccessClasses.show_busy:
                s = _("Busy")
            s = event.user.username + ': ' + unicode(s)
        elif settings.SITE.project_model is not None \
                and event.project is not None:
            s += " " + unicode(_("with")) + " " + unicode(event.project)
        if event.state:
            s = ("(%s) " % unicode(event.state)) + s
        n = event.guest_set.all().count()
        if n:
            s = ("[%d] " % n) + s
        return s

    def before_ui_save(self, ar, **kw):
        """Mark the event as "user modified" by setting a default state.
        This is important because EventGenerators may not modify any
        user-modified Events.

        """
        # logger.info("20130528 before_ui_save")
        if self.state is EntryStates.suggested:
            self.state = EntryStates.draft
        return super(Event, self).before_ui_save(ar, **kw)

    def on_create(self, ar):
        self.event_type = ar.user.event_type or \
            settings.SITE.site_config.default_event_type
        self.start_date = settings.SITE.today()
        self.start_time = timezone.now().time()
        # see also Assignable.on_create()
        super(Event, self).on_create(ar)

    # def on_create(self,ar):
        # self.start_date = settings.SITE.today()
        # self.start_time = datetime.datetime.now().time()
        # ~ # default user is almost the same as for UserAuthored
        # ~ # but we take the *real* user, not the "working as"
        # if self.user_id is None:
            # u = ar.user
            # if u is not None:
                # self.user = u
        # super(Event,self).on_create(ar)

    def get_postable_recipients(self):
        """return or yield a list of Partners"""
        if self.project:
            if isinstance(self.project, dd.plugins.cal.partner_model):
                yield self.project
        for g in self.guest_set.all():
            yield g.partner
        # if self.user.partner:
            # yield self.user.partner

    def get_mailable_type(self):
        return self.event_type

    def get_mailable_recipients(self):
        if self.project:
            if isinstance(self.project, dd.plugins.cal.partner_model):
                yield ('to', self.project)
        for g in self.guest_set.all():
            yield ('to', g.partner)
        if self.user.partner:
            yield ('cc', self.user.partner)

    # def get_mailable_body(self,ar):
        # return self.description

    @dd.displayfield(_("When"))
    def when_text(self, ar):
        txt = when_text(self.start_date, self.start_time)
        if self.end_date and self.end_date != self.start_date:
            txt += "-" + when_text(self.end_date, self.end_time)
        return txt

    @dd.displayfield(_("When"))
    # def linked_date(self, ar):
    def when_html(self, ar):
        if ar is None:
            return ''
        EntriesByDay = settings.SITE.modules.cal.EntriesByDay
        txt = when_text(self.start_date, self.start_time)
        return EntriesByDay.as_link(ar, self.start_date, txt)
        # return self.obj2href(ar, txt)

    @dd.displayfield(_("Link URL"))
    def url(self, ar):
        return 'foo'

    @dd.virtualfield(dd.DisplayField(_("Reminder")))
    def reminder(self, request):
        return False
    # reminder.return_type = dd.DisplayField(_("Reminder"))

    def get_calendar(self):
        """
        Returns the Calendar which contains this event,
        or None if no subscription is found.
        Needed for ext.ensible calendar panel.

        The default implementation returns None.
        Override this if your app uses Calendars.
        """
        # for sub in Subscription.objects.filter(user=ar.get_user()):
            # if sub.contains_event(self):
                # return sub
        return None

    @dd.virtualfield(models.ForeignKey('cal.Calendar'))
    def calendar(self, ar):
        return self.get_calendar()

    def get_print_language(self):
        # if settings.SITE.project_model is not None and self.project:
        if self.project:
            return self.project.get_print_language()
        if self.user:
            return self.user.language
        return settings.SITE.get_default_language()

    @classmethod
    def get_default_table(cls):
        return OneEvent

    @classmethod
    def on_analyze(cls, lino):
        cls.DISABLED_AUTO_FIELDS = dd.fields_list(cls, "summary")
        super(Event, cls).on_analyze(lino)

    def auto_type_changed(self, ar):
        """When the number has changed, we must update the summary."""
        if self.auto_type:
            self.summary = self.owner.update_cal_summary(
                self.event_type, self.auto_type)

dd.update_field(Event, 'user', verbose_name=_("Responsible user"))


class EntryChecker(Checker):
    model = Event
    def get_responsible_user(self, obj):
        return obj.user or super(
            EntryChecker, self).get_responsible_user(obj)
    
class EventGuestChecker(EntryChecker):
    """Check for calendar entries without participants.

    :message:`No participants although N suggestions exist.` --
    This is probably due to some problem in the past, so we repair
    this by adding the suggested guests.

    """
    verbose_name = _("Entries without participants")

    def get_plausibility_problems(self, obj, fix=False):
        if not obj.state.edit_guests:
            return
        existing = set([g.partner.pk for g in obj.guest_set.all()])
        if len(existing) == 0:
            suggested = list(obj.suggest_guests())
            if len(suggested) > 0:
                msg = _("No participants although {0} suggestions exist.")
                yield (True, msg.format(len(suggested)))
                if fix:
                    for g in suggested:
                        g.save()

EventGuestChecker.activate()


class ConflictingEventsChecker(EntryChecker):
    """Check whether this entry conflicts with other events.

    """
    verbose_name = _("Check for conflicting calendar entries")

    def get_plausibility_problems(self, obj, fix=False):
        if not obj.has_conflicting_events():
            return
        qs = obj.get_conflicting_events()
        num = qs.count()
        if num == 1:
            msg = _("Event conflicts with {0}.").format(qs[0])
        else:
            msg = _("Event conflicts with {0} other events.").format(num)
        yield (False, msg)

ConflictingEventsChecker.activate()


class ObsoleteEventTypeChecker(EntryChecker):
    """Check whether the type of this calendar entry should be updated.

    This can happen when the configuration has changed and there are
    automatic entries which had been generated using the old
    configuration.

    """
    verbose_name = _("Obsolete event type of generated entries")

    def get_plausibility_problems(self, obj, fix=False):
        if not obj.auto_type:
            return
        et = obj.owner.update_cal_event_type()
        if obj.event_type != et:
            msg = _("Event type but {0} (should be {1}).").format(
                obj.event_type, et)
            yield (False, msg)
            if fix:
                obj.event_type = et
                obj.full_clean()
                obj.save()

ObsoleteEventTypeChecker.activate()


class LongEntryChecker(EntryChecker):
    """Check for entries which last longer than the maximum number of days
    allowed by their type.

    """
    verbose_name = _("Too long-lasting calendar entries")
    model = Event

    def get_plausibility_problems(self, obj, fix=False):
        if obj.end_date is None:
            return
        et = obj.event_type
        if et is None:
            return
        duration = obj.end_date - obj.start_date
        
        # print (20161222, duration.days, et.max_days)
        if duration.days > et.max_days:
            msg = _("Event lasts {0} days but only {1} are allowed.").format(
                duration.days, et.max_days)
            yield (True, msg)
            if fix:
                obj.end_date = None
                obj.full_clean()
                obj.save()

LongEntryChecker.activate()


@dd.python_2_unicode_compatible
class Guest(dd.Model):
    workflow_state_field = 'state'
    allow_cascaded_delete = ['event']

    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Guest')
        # verbose_name = _("Participant")
        # verbose_name_plural = _("Participants")
        verbose_name = _("Presence")
        verbose_name_plural = _("Presences")
        unique_together = ['event', 'partner']

    event = models.ForeignKey('cal.Event')
    partner = dd.ForeignKey(dd.plugins.cal.partner_model)
    role = models.ForeignKey(
        'cal.GuestRole', verbose_name=_("Role"), blank=True, null=True)
    state = GuestStates.field(default=GuestStates.invited.as_callable)
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    # Define a `user` property because we want to use
    # `lino.modlib.users.mixins.My`
    def get_user(self):
        # used to apply `owner` requirement in GuestState
        return self.event.user
    user = property(get_user)
    # author_field_name = 'user'

    def __str__(self):
        return u'%s #%s (%s)' % (
            self._meta.verbose_name, self.pk, self.event.strftime())

    # def get_printable_type(self):
    #     return self.role

    def get_mailable_type(self):
        return self.role

    def get_mailable_recipients(self):
        yield ('to', self.partner)

    @dd.displayfield(_("Event"))
    def event_summary(self, ar):
        if ar is None:
            return ''
        return ar.obj2html(self.event, self.event.get_event_summary(ar))


def migrate_reminder(obj, reminder_date, reminder_text,
                     delay_value, delay_type, reminder_done):
    """
    This was used only for migrating to 1.2.0,
    see :mod:`lino.projects.pcsw.migrate`.
    """
    raise NotImplementedError(
        "No longer needed (and no longer supported after 20111026).")

    def delay2alarm(delay_type):
        if delay_type == 'D':
            return DurationUnits.days
        if delay_type == 'W':
            return DurationUnits.weeks
        if delay_type == 'M':
            return DurationUnits.months
        if delay_type == 'Y':
            return DurationUnits.years

    # ~ # These constants must be unique for the whole Lino Site.
    # ~ # Keep in sync with auto types defined in lino.projects.pcsw.models.Person
    # REMINDER = 5

    if reminder_text:
        summary = reminder_text
    else:
        summary = _('due date reached')

    update_auto_task(
        None,  # REMINDER,
        obj.user,
        reminder_date,
        summary, obj,
        done=reminder_done,
        alarm_value=delay_value,
        alarm_unit=delay2alarm(delay_type))


# Inject application-specific fields to users.User.
dd.inject_field(settings.SITE.user_model,
                'access_class',
                AccessClasses.field(
                    default=AccessClasses.public.as_callable,
                    verbose_name=_("Default access class"),
                    help_text=_(
            """The default access class for your calendar events and tasks.""")
                ))
dd.inject_field(settings.SITE.user_model,
                'event_type',
                models.ForeignKey('cal.EventType',
                                  blank=True, null=True,
                                  verbose_name=_("Default Event Type"),
        help_text=_("""The default event type for your calendar events.""")
                ))

dd.inject_field(
    'system.SiteConfig',
    'default_event_type',
    models.ForeignKey(
        'cal.EventType',
        blank=True, null=True,
        verbose_name=_("Default Event Type"),
        help_text=_("""The default type of events on this site.""")
    ))

dd.inject_field(
    'system.SiteConfig',
    'site_calendar',
    models.ForeignKey(
        'cal.Calendar',
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_site_calender",
        verbose_name=_("Site Calendar"),
        help_text=_("""The default calendar of this site.""")))

dd.inject_field(
    'system.SiteConfig',
    'max_auto_events',
    models.IntegerField(
        _("Max automatic events"), default=72,
        blank=True, null=True,
        help_text=_(
            """Maximum number of automatic events to be generated.""")
    ))

dd.inject_field(
    'system.SiteConfig',
    'hide_events_before',
    models.DateField(
        _("Hide events before"),
        blank=True, null=True,
        help_text=_("""If this is specified, certain tables show only 
events after the given date.""")
    ))


Reservation.show_today = ShowEntriesByDay('start_date')

if False:  # removed 20160610 because it is probably not used

    def update_reminders_for_user(user, ar):
        n = 0
        for model in rt.models_by_base(EventGenerator):
            for obj in model.objects.filter(user=user):
                obj.update_reminders(ar)
                # logger.info("--> %s",unicode(obj))
                n += 1
        return n

    class UpdateUserReminders(UpdateEntries):

        """
        Users can invoke this to re-generate their automatic tasks.
        """

        def run_from_ui(self, ar, **kw):
            user = ar.selected_rows[0]
            dd.logger.info("Updating reminders for %s", unicode(user))
            n = update_reminders_for_user(user, ar)
            msg = _("%(num)d reminders for %(user)s have been updated."
                    ) % dict(user=user, num=n)
            dd.logger.info(msg)
            ar.success(msg, **kw)

    @dd.receiver(dd.pre_analyze, dispatch_uid="add_update_reminders")
    def pre_analyze(sender, **kw):
        sender.user_model.define_action(update_reminders=UpdateUserReminders())


from .ui import *

