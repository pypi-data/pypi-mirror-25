# -*- coding: utf-8 -*-

from django.apps import AppConfig


class NavsyConfig(AppConfig):

    name = 'navsy'
    verbose_name = 'Navigation'

    def ready(self):

        from navsy import settings, signals

        settings.check_settings()

        try:
            signals.post_migrate_app(self)
        except Exception:
            pass
