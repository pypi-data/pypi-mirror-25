# -*- coding: UTF-8 -*-
# Copyright 2008-2017 Luc Saffre
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

from lino.api import dd, rt, _
from lino import mixins

from lino.utils import join_words
from lino.utils import join_elems

from lino_xl.lib.countries.mixins import AddressLocation
from lino_xl.lib.phones.mixins import ContactDetailsOwner

from lino.utils.xmlgen.html import E
from lino.utils.addressable import Addressable
from lino.mixins.periods import ObservedDateRange


from .mixins import ContactRelated, PartnerDocument, OldCompanyContact
# from lino.mixins import Contactable, Phonable
from .roles import SimpleContactsUser, ContactsStaff
from .choicelists import PartnerEvents

from lino.mixins.human import name2kw, Human, Born


PARTNER_NUMBERS_START_AT = 100  # used for generating demo data and tests


@dd.python_2_unicode_compatible
class Partner(ContactDetailsOwner, mixins.Polymorphic, AddressLocation):
    preferred_foreignkey_width = 20
    # preferred width for ForeignKey fields to a Partner

    class Meta(object):
        app_label = 'contacts'  # avoid RemovedInDjango19Warning
        abstract = dd.is_abstract_model(__name__, 'Partner')
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    prefix = models.CharField(
        _("Name prefix"), max_length=200, blank=True)

    name = models.CharField(max_length=200, verbose_name=_('Name'))

    remarks = models.TextField(_("Remarks"), blank=True)  # ,null=True)

    quick_search_fields = "prefix name phone gsm"

    # print_labels = dd.PrintLabelsAction()

    def on_create(self, ar):
        self.language = ar.get_user().language
        if not self.country:
            sc = settings.SITE.site_config
            if sc.site_company:
                self.country = sc.site_company.country
        super(Partner, self).on_create(ar)

    def save(self, *args, **kw):
        if self.id is None:
            sc = settings.SITE.site_config
            if sc.next_partner_id is not None:
                try:
                    self.__class__.objects.get(id=sc.next_partner_id)
                    raise ValidationError(
                        "Cannot create partner with id={0}. "
                        "Check your next_partner_id in SiteConfig!".format(
                            sc.next_partner_id))
                except self.__class__.DoesNotExist:
                    self.id = sc.next_partner_id
                    sc.next_partner_id += 1
                    sc.save()
        #~ logger.info("20120327 Partner.save(%s,%s)",args,kw)
        super(Partner, self).save(*args, **kw)

    def get_last_name_prefix(self):
        # overrides lino.mixins.humans.Human
        return self.prefix
    
    def __str__(self):
        #~ return self.name
        return self.get_full_name()

    def address_person_lines(self):
        #~ yield self.name
        yield self.get_full_name()

    def get_full_name(self, *args, **kwargs):
        """Return a one-line string representing this Partner.  The default
        returns simply the `name`, optionally prefixed by the
        :attr:`prefix`, ignoring any arguments, but
        e.g. :class:`Human` overrides this.

        """
        return join_words(self.prefix, self.name)
    full_name = property(get_full_name)

    @dd.displayfield(_("Name"))
    def name_column(self, request):
        return str(self)

    def get_partner_instance(self):
        return self  # compatibility with lino.modlib.partners

    def get_overview_elems(self, ar):
        elems = []
        buttons = self.get_mti_buttons(ar)
        # buttons = join_elems(buttons, ', ')
        elems.append(E.p(str(_("See as ")), *buttons,
                         style="font-size:8px;text-align:right;padding:3pt;"))
        elems += self.get_name_elems(ar)
        elems.append(E.br())
        elems += join_elems(list(self.address_location_lines()), sep=E.br)
        elems = [
            E.div(*elems,
                  style="font-size:18px;font-weigth:bold;"
                  "vertical-align:bottom;text-align:middle")]
        return elems

    def get_name_elems(self, ar):
        return [E.b(self.name)]

    def get_print_language(self):
        return self.language

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(
            observed_event=PartnerEvents.field(
                blank=True,
                help_text=_("Extended filter criteria")))
        super(Partner, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(Partner, self).get_request_queryset(ar, **filter)

        pv = ar.param_values
        oe = pv.observed_event
        if oe:
            qs = oe.add_filter(qs, pv)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Partner, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        if pv.observed_event:
            yield str(pv.observed_event)


    def get_as_user(self):
        """Return the user object that corresponds to this partner.

        If the application's User model inherits from Partner, then
        

        """
        User = rt.models.users.User
        try:
            if issubclass(User, self.__class__):
                return User.objects.get(partner_ptr=self)
            else:
                return User.objects.get(partner=self)
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            pass
        
class PartnerDetail(dd.DetailLayout):

    main = """
    address_box:60 contact_box:30 overview
    bottom_box
    """

    address_box = dd.Panel("""
    name_box
    country region city zip_code:10
    addr1
    #street_prefix street:25 street_no street_box
    addr2
    """, label=_("Address"))

    contact_box = dd.Panel("""
    info_box
    email:40
    url
    phone
    gsm fax
    """, label=_("Contact"))

    bottom_box = """
    remarks
    """

    name_box = "#prefix name"
    info_box = "id language"


class Partners(dd.Table):
    required_roles = dd.login_required(SimpleContactsUser)
    model = 'contacts.Partner'
    column_names = "name email * id"
    order_by = ['name', 'id']
    parameters = ObservedDateRange()
    detail_layout = PartnerDetail()
    insert_layout = """
    name
    #language email
    """

    @classmethod
    def get_queryset(self, ar):
        qs = super(Partners, self).get_queryset(ar)
        return qs.select_related('country', 'city')
        # return self.model.objects.select_related('country', 'city')


#~ class AllPartners(Partners):

    #~ @classmethod
    #~ def get_actor_label(self):
        #~ return _("All %s") % self.model._meta.verbose_name_plural

class PartnersByCity(Partners):
    master_key = 'city'
    order_by = 'street street_no street_box addr2'.split()
    column_names = "address_column #street #street_no #street_box #addr2 name *"


class PartnersByCountry(Partners):
    master_key = 'country'
    column_names = "city street street_no name language *"
    order_by = "city street street_no".split()


class Person(Human, Born, Partner):
    class Meta(object):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['last_name', 'first_name']

    def get_after_salutation_words(self):
        if self.prefix:
            yield self.prefix
            
    def full_clean(self, *args, **kw):
        """Set the `name` field of this person.  This field is visible in the
        Partner's detail but not in the Person's detail and serves for
        sorting when selecting a Partner.  It also serves for quick
        search on Persons.

        """
        name = join_words(self.last_name, self.first_name)
        if name:
            self.name = name
        else:
            for k, v in list(name2kw(self.name).items()):
                setattr(self, k, v)
            # self.last_name = self.name
        super(Person, self).full_clean(*args, **kw)

    def address_person_lines(self, *args, **kw):
        "Deserves more documentation."
        # if self.title:
        #     yield join_words(self.get_salutation(), self.title)
        #     kw.update(salutation=False)
        yield self.get_full_name(*args, **kw)

    def get_name_elems(self, ar):
        elems = [self.get_salutation(nominative=True), ' ',
                 self.prefix, E.br()]
        elems += [self.first_name, ' ', E.b(self.last_name)]
        return elems


class PersonDetail(PartnerDetail):

    name_box = "last_name first_name:15 gender #prefix:10"
    info_box = "id:5 language:10"
    bottom_box = "remarks contacts.RolesByPerson"


class Persons(Partners):
    required_roles = dd.login_required(SimpleContactsUser)
    model = "contacts.Person"
    order_by = ["last_name", "first_name", "id"]
    column_names = (
        "name_column:20 address_column email "
        "phone:10 gsm:10 id language:10 *")
    detail_layout = PersonDetail()

    insert_layout = """
    first_name last_name
    gender email #language
    """


class CompanyType(mixins.BabelNamed):
    class Meta(object):
        app_label = 'contacts'  # avoid RemovedInDjango19Warning
        abstract = dd.is_abstract_model(__name__, 'CompanyType')
        verbose_name = _("Organization type")
        verbose_name_plural = _("Organization types")

    abbr = dd.BabelCharField(_("Abbreviation"), max_length=30, blank=True)


class CompanyTypes(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'contacts.CompanyType'
    column_names = 'name *'
    #~ label = _("Company types")


class Company(Partner):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'Company')
        app_label = 'contacts'
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    type = models.ForeignKey('contacts.CompanyType', blank=True, null=True)

    def get_full_name(self, salutation=True, **salutation_options):
        """Deserves more documentation."""
        #~ print '20120729 Company.get_full_name`'
        if self.type:
            return join_words(self.prefix, self.type.abbr, self.name)
        return join_words(self.prefix, self.name)
    full_name = property(get_full_name)

    def get_name_elems(self, ar):
        elems = []
        if self.prefix:
            elems += [self.prefix, ' ']
        elems += [E.b(self.name)]
        return elems


class CompanyDetail(PartnerDetail):

    bottom_box = """
    remarks contacts.RolesByCompany
    """

    name_box = "prefix:10 name type:30"


class Companies(Partners):
    required_roles = dd.login_required(SimpleContactsUser)
    model = "contacts.Company"
    order_by = ["name"]
    column_names = (
        "name_column:20 address_column email "
        "phone:10 gsm:10 id language:10 *")
    detail_layout = CompanyDetail()
    insert_layout = """
    name
    #language:20 email:40
    type id
    """

#~ class List(Partner):
    #~ pass

#~ class Lists(Partners):
    #~ model = List
    #~ order_by = ["name"]
    #~ detail_layout = """
    #~ id name
    #~ language email
    #~ MembersByList
    #~ """
    #~ insert_layout = dd.FormLayout("""
    #~ name
    #~ language email
    #~ """,window_size=(40,'auto'))


# class ContactType(mixins.BabelNamed):
class RoleType(mixins.BabelNamed):

    class Meta(object):
        app_label = 'contacts'  # avoid RemovedInDjango19Warning
        abstract = dd.is_abstract_model(__name__, 'RoleType')
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")


class RoleTypes(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'contacts.RoleType'


@dd.python_2_unicode_compatible
class Role(dd.Model, Addressable):

    class Meta(object):
        app_label = 'contacts'  # avoid RemovedInDjango19Warning
        abstract = dd.is_abstract_model(__name__, 'Role')
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")

    type = models.ForeignKey(
        'contacts.RoleType',
        blank=True, null=True,
        verbose_name=_("Contact Role"))
    person = models.ForeignKey(
        "contacts.Person", related_name='rolesbyperson')
    company = models.ForeignKey(
        "contacts.Company", related_name='rolesbycompany')

    def __str__(self):
        if self.person_id is None:
            return super(Role, self).__str__()
        if self.type is None:
            return str(self.person)
        return u"%s (%s)" % (self.person, self.type)

    def address_person_lines(self):
        if self.company:
            for ln in self.company.address_person_lines():
                yield ln
        for ln in self.person.address_person_lines():
            yield ln

    def address_location_lines(self):
        if self.company_id:
            return self.company.address_location_lines()
        if self.person_id:
            return self.person.address_location_lines()
        return super(Role, self).__str__()

    def get_print_language(self):
        if self.company_id:
            return self.company.language
        if self.person_id:
            return self.person.language
        return super(Role, self).get_print_language()


class Roles(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'contacts.Role'


class RolesByCompany(Roles):
    required_roles = dd.login_required(SimpleContactsUser)
    auto_fit_column_widths = True
    #~ required_user_level = None
    label = _("Contact persons")
    master_key = 'company'
    column_names = 'person type *'
    hidden_columns = 'id'


class RolesByPerson(Roles):
    """Shows all roles of a person."""
    required_roles = dd.login_required(SimpleContactsUser)
    #~ required_user_level = None
    label = _("Contact for")
    master_key = 'person'
    column_names = 'company type *'
    auto_fit_column_widths = True
    hidden_columns = 'id'

dd.inject_field(
    'system.SiteConfig',
    'next_partner_id',
    models.IntegerField(
        default=PARTNER_NUMBERS_START_AT,
        blank=True, null=True,
        verbose_name=_("Next partner id"),
        help_text=_("The next automatic id for any new partner.")))


def unused_site_setup(site):

    site.modules.countries.Places.set_detail_layout("""
    name country
    type parent zip_code id
    PlacesByPlace
    contacts.PartnersByCity
    """)


@dd.receiver(dd.pre_analyze)
def company_model_alias(sender, **kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisation = sender.modules.contacts.Company


@dd.receiver(dd.post_analyze)
def company_tables_alias(sender, **kw):
    """
    prepare ticket #72 which will rename Company to Organisation
    """
    sender.modules.contacts.Organisations = sender.modules.contacts.Companies


def PartnerField(**kw):
    return models.ForeignKey(Partner, **kw)
