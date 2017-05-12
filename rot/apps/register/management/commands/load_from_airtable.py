# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management import BaseCommand

import requests

from person.models import Person
from register.models import Item, Category


class AirTableClient:
    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.key = key
        self.data = {}

    def get(self, table):
        if table not in self.data:
            headers = {
                'Authorization': 'Bearer {key}'.format(key=self.key)
            }
            url = '{base}{table}'.format(base=self.endpoint, table=table)
            resp = requests.get(url, headers=headers)
            self.data[table] = resp.json()['records']
        return self.data[table]

    def get_record_by_id(self, table, id):
        if table not in self.data:
            self.get(table)
        item = next(iter(filter(lambda x: x['id'] == id, self.data[table])))
        return item['fields']


class Command(BaseCommand):
    help = "Loads MVP data in from Airtable"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.airtable = AirTableClient(
            settings.AIRTABLE_API,
            settings.AIRTABLE_API_KEY)

    def handle(self, *args, **options):
        self._load('Category', self._load_Category)
        self._load('Person', self._load_person)
        self._load('Service', self._load_item)

    def _load(self, table, load_func):
        records = self.airtable.get(table)

        for record in records:
            id = record['id']
            record = record['fields']
            if record:
                load_func(record, table, id)

    def _load_Category(self, record, table, id):
        category, created = Category.objects.get_or_create(name=record['Name'])

        if record.get('Parent'):
            parent_record = self.airtable.get_record_by_id(
                table, record.get('Parent')[0])
            parent, pcreated = Category.objects.get_or_create(
                name=parent_record['Name'])
            category.parent = parent
        schema = {

        }
        category.airtable_id = id
        category.schema = schema
        category.save()

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

        item, created = Item.objects.get_or_create(
            name=record['Name'],
            description=record.get('Description'),
            owner=owner,
            category=category,
            data={},
        )

        item.airtable_id = id
        item.save()
