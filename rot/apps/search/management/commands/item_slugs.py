# -*- coding: utf-8 -*-

from django.core.management import BaseCommand

from register.models import Item


class Command(BaseCommand):
    help = "Sets the slug parameter on Item for all records"

    def handle(self, *args, **options):
        for i in Item.objects.all():
            i.save()
            self.stdout.write('{} {}'.format(i.slug, i.name))
