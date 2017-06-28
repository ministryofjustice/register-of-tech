# -*- coding: utf-8 -*-
from collections import defaultdict

from django.conf import settings
from django.core.management import BaseCommand

from airtable.airtable import Airtable

from person.models import Person
from register.models import Item, Category, BusinessArea


class Command(BaseCommand):
    help = "Loads and writes MVP data from Airtable"

    def __init__(self):
        super().__init__()
        self.airtable = None
        self._cache = defaultdict(dict)

    def add_arguments(self, parser):
        parser.add_argument(
            'action', choices=['get', 'put'],
            help='get from airtable or write to airtable')

    def handle(self, *args, **options):
        if options['action'] == 'put':
            self._write_all()
        elif options['action'] == 'get':
            self._load_all()

    def _write_all(self):
        self.airtable = Airtable(
            settings.AIRTABLE_WRITE_API_ID,
            settings.AIRTABLE_API_KEY)
        self._write(BusinessArea, 'Organisation', self._write_business_area)
        self._write(Category, 'Category', self._write_category)
        self._write(Person, 'Person', self._write_person)
        self._write(Item, 'Service', self._write_item)

    def _delete_all_from_table(self, table):
        for record in self.airtable.iterate(table, view='Grid view'):
            self.airtable.delete(table, record['id'])

    def _write(self, model, table, write_func):
        self._delete_all_from_table(table)
        for obj in model.objects.all():
            try:
                created = self.airtable.create(table, write_func(obj))
                self._cache[table][created['id']] = created
                obj.airtable_id = created['id']
                obj.save()
            except Exception as e:
                self.stderr.write(e)
                self.stderr.write(
                    'Failed to write {data}'.format(data = write_func(obj)))

    def _write_business_area(self, obj):
        parents = []
        if obj.parent:
            parents = [obj.parent.airtable_id]
        return {
            'Name': obj.name,
            'Description': obj.description,
            "Parent": parents,
        }

    def _write_category(self, obj):
        parents = []
        if obj.parent:
            parents = [obj.parent.airtable_id]
        return {
            'Name': obj.name,
            "Parent": parents,
        }

    def _write_person(self, obj):
        return {
            'Name': '{first} {last}'.format(
                first=obj.first_name, last=obj.last_name),
            'Email': obj.email,
            'People Finder link': obj.peoplefinder
        }

    def _write_item(self, obj):
        return {
            'Name': obj.name,
            'Description': obj.description,
            'Owner': [obj.owner.airtable_id],
            'Service Category': [obj.category.airtable_id],
            'Organisation': [obj.area.airtable_id],
        }

    def _load_all(self):
        self.airtable = Airtable(
            settings.AIRTABLE_API_ID,
            settings.AIRTABLE_API_KEY)
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
        if record.get('Name'):
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
                data={},
            )

            # TODO - Allow adding multiple categories and areas from airtable
            item.categories.add(category)
            item.areas.add(business_area)

            item.airtable_id = id
            item.save()
