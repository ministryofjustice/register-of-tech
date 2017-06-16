# -*- coding: utf-8 -*-
import os

from django.core.management import BaseCommand

from person.models import Person
from oauth2_provider.models import Application


class Command(BaseCommand):
    help = "Sets secrets on Superuser and Application"

    def handle(self, *args, **options):
        self._set_superuser_password()
        self._set_application_secrets()

    def _set_superuser_password(self):
        if os.environ.get('SUPERUSER_PASSWORD'):
            person, created = Person.objects.get_or_create(username='super')
            if created:
                person.first_name = 'Super'
                person.last_name = 'User'
                person.email = os.environ.get('DEFAULT_EMAIL_FROM')
            person.password = os.environ.get('SUPERUSER_PASSWORD')
            person.save()

    def _set_application_secrets(self):
        if os.environ.get('SUPERUSER_PASSWORD'):
            application = Application.objects.get(pk=1)
            application.client_id = os.environ.get('CLIENT_ID')
            application.client_secret = os.environ.get('CLIENT_SECRET')
            application.save()
