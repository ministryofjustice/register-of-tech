# -*- coding: utf-8 -*-
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Integer, Text, Date
from elasticsearch_dsl.connections import connections

from register.models import Item


connections.create_connection(hosts=[settings.ELASTICSEARCH_ENDPOINT])


class BaseSearchIndexMixin:
    @classmethod
    def index(cls, obj):
        index = cls.create(obj)
        index.save()
        return index.to_dict(include_meta=True)

    @classmethod
    def delete_index(cls, obj):
        index = cls.create(obj)
        index.delete()

    @classmethod
    def bulk_index(cls):
        es = Elasticsearch()
        cls.init()
        bulk(client=es, actions=(cls.index(b) for b in
                                 cls.queryset.iterator()))


class ItemIndex(DocType, BaseSearchIndexMixin):
    queryset = Item.objects.all()

    pk = Integer()
    name = Text()
    description = Text()
    categories = Text(multi=True)
    areas = Text(multi=True)
    owner = Text()
    created = Date()
    modified = Date()

    class Meta:
        index = 'item'

    @classmethod
    def create(cls, obj):
        return cls(
            meta={'id': obj.pk},
            name=obj.name,
            description=obj.description,
            categories=[c.name for c in obj.categories.all()],
            areas=[a.name for a in obj.areas.all()],
            owner=obj.owner.get_full_name(),
            created=obj.created,
            modified=obj.modified,
        )




