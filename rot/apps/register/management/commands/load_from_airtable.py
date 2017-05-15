# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import BaseCommand

from airtable.airtable import Airtable

from person.models import Person
from register.models import Item, Category, BusinessArea


class Command(BaseCommand):
    help = "Loads MVP data in from Airtable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.airtable = Airtable(
            settings.AIRTABLE_API_ID,
            settings.AIRTABLE_API_KEY)

    def handle(self, *args, **options):
        self._load('Organisation', self._load_business_area)
        self._load('Category', self._load_category)
        self._load('Person', self._load_person)
        self._load('Service', self._load_item)

    def _load(self, table, load_func):
        for record in self.airtable.iterate(table, view='Grid view'):
            id = record['id']
            record = record['fields']
            if record:
                load_func(record, table, id)

    def _load_category(self, record, table, id):
        category, created = Category.objects.get_or_create(
            name=record['Name'])

        if record.get('Parent'):
            parent = Category.objects.get(airtable_id=record.get('Parent')[0])
            category.parent = parent
        schema = {

        }
        category.airtable_id = id
        category.schema = schema
        category.save()

    def _load_business_area(self, record, table, id):
        business_area, created = BusinessArea.objects.get_or_create(
            name=record['Name'])

        if record.get('Parent'):
            parent = BusinessArea.objects.get(
                airtable_id=record.get('Parent')[0])
            business_area.parent = parent
        business_area.airtable_id = id
        business_area.description = record.get('Description')
        business_area.save()

    def _load_person(self, record, table, id):
        names = record['Name'].split(', ')
        for name in names:
            first_name, last_name, *rest = map(lambda x: x.strip(),
                                               name.split())
            username = '{first}.{last}'.format(
                first=first_name, last=last_name)
            email = '{username}@digital.justice.gov.uk'.format(
                username=username).lower()

            person, created = Person.objects.get_or_create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            person.airtable_id = id
            person.save()

    def _load_item(self, record, table, id):
        owner = None
        if record.get('Owner'):
            owner_id = record['Owner'][0]
            owners = Person.objects.filter(airtable_id=owner_id)
            if owners:
                owner = owners[0]
        if not owner:
            owner = Person.objects.get(pk=2)

        if record.get('Service Category'):
            category_id = record['Service Category'][0]
            category = Category.objects.filter(airtable_id=category_id)[0]
        else:
            category = Category.objects.get(pk=1)

        if record.get('Organisation'):
            business_area_id = record['Organisation'][0]
            business_area = BusinessArea.objects.filter(
                airtable_id=business_area_id)[0]
        else:
            business_area = BusinessArea.objects.get(pk=1)

        item, created = Item.objects.get_or_create(
            name=record['Name'],
            description=record.get('Description'),
            owner=owner,
            category=category,
            area=business_area,
            data={},
        )

        item.airtable_id = id
        item.save()
