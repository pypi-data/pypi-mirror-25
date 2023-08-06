# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig as DJAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(DJAppConfig):
    name = 'nimubs_api'
    verbose_name = _('Nimbus API')
