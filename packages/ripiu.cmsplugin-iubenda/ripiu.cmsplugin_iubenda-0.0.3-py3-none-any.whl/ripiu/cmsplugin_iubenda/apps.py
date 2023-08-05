# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class IubendaConfig(AppConfig):
    name = 'ripiu.cmsplugin_iubenda'
    verbose_name = _('Iubenda integration')
