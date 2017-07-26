# -*- coding: utf-8 -*-
from django.apps import AppConfig


class RegisterAppConfig(AppConfig):
    name = 'search'

    def ready(self):
        from search import signals
