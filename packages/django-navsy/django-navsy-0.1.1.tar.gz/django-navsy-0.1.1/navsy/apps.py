# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.utils import OperationalError


class NavsyConfig(AppConfig):

    name = 'navsy'
    verbose_name = 'Navigation'

    def ready(self):

        from navsy import cache, settings, signals
        from navsy.models import Page, Pattern

        settings.check_settings()

        try:
            Pattern.create_default_objects()
            Page.create_first_object()

            cache.update_data()

        except OperationalError:
            # until "python manage.py migrate nav"
            pass
