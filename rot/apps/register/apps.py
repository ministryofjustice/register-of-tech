from django.apps import AppConfig


class RegisterAppConfig(AppConfig):
    name = 'register'

    def ready(self):
        from register import signals
