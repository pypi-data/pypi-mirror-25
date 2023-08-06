# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds the notions of "skills", including offers and demands thereof.

.. autosummary::
   :toctree:

   models
   ui
   roles

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """.. attribute:: demander_model

        The model of objects to be used as :attr:`demander
        <lino_xl.lib.faculties.models.Demand.demander>` of skill
        demands. 

        In :ref:`noi` this points to :class:`Ticket
        <lino_xl.lib.tickets.models.Ticket>`.


    """

    verbose_name = _("Skills")

    needs_plugins = [
        # 'lino_noi.lib.noi',
        'lino_xl.lib.xl',
        # 'lino_xl.lib.tickets',
        'lino_noi.lib.contacts']

    # demander_model = 'tickets.Ticket'
    # demander_model = 'contacts.Person'
    # supplier_model = 'contacts.Person'
    demander_model = 'contacts.Partner'
    # supplier_model = 'contacts.Partner'

    # end_user_model = 'users.User'
    end_user_model = 'contacts.Partner'

    def on_site_startup(self, site):
        self.end_user_model = site.models.resolve(self.end_user_model)
        self.demander_model = site.models.resolve(self.demander_model)
        # self.supplier_model = site.models.resolve(self.supplier_model)
        super(Plugin, self).on_site_startup(site)
        
    def get_menu_group(self):
        return self
        # return self.site.plugins.get(
        #     self.demander_model._meta.app_label)
    
    def setup_main_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        # mg = site.plugins.tickets
        m = m.add_menu(mg.app_label, mg.verbose_name)
        # m.add_action('faculties.Faculties')
        # m.add_action('faculties.Competences')
        m.add_action('faculties.MyOffers')

    def setup_config_menu(self, site, user_type, m):
        mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('faculties.TopLevelSkills')
        m.add_action('faculties.AllSkills')
        m.add_action('faculties.SkillTypes')

    def setup_explorer_menu(self, site, user_type, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        # m.add_action('faculties.Competences')
        m.add_action('faculties.Offers')
        m.add_action('faculties.Demands')

    def get_dashboard_items(self, user):
        if user.authenticated:
            if self.site.is_installed('tickets'):
                yield self.site.models.faculties.SuggestedTicketsByEndUser
