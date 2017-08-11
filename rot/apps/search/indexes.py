# -*- coding: utf-8 -*-
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import (
    Date,
    DocType,
    FacetedSearch,
    Integer,
    Keyword,
    Text,
    analyzer,
    tokenizer,
    TermsFacet,
)
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.field import Object

from register.models import Item

connections.create_connection(hosts=[settings.ELASTICSEARCH_ENDPOINT])

ngram_analyzer = analyzer('ngram_analyzer',
                          tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
                          filter=['lowercase']
                          )


class NgramText(Text):
    def __init__(self, *args, **kwargs):
        if 'analyzer' not in kwargs:
            kwargs['analyzer'] = ngram_analyzer
        super().__init__(*args, **kwargs)


class BaseSearchIndexMixin:
    def prepare(self, obj):
        raise NotImplementedError(
            'Override this method to return a dict of fields')

    def _prepare(self, obj):
        self.__init__(
            **self.prepare(obj)
        )

    @classmethod
    def index(cls, obj):
        index = cls()
        index._prepare(obj)
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

    name = NgramText(fields={'raw': Keyword()})
    slug = Keyword(index=False)
    description = NgramText()
    categories = Keyword(multi=True)
    areas = Keyword(multi=True)
    owner = Text(fields={'raw': Keyword()})

    class Meta:
        index = 'item'

    def prepare(self, obj):
        return dict(
            meta={'id': obj.pk},
            name=obj.name,
            slug=obj.slug,
            description=obj.description,
            categories=[c.name for c in obj.categories.all()],
            areas=[a.name for a in obj.areas.all()],
            owner=obj.owner.get_full_name(),
        )


class ItemSearch(FacetedSearch):
    doc_types = [ItemIndex, ]

    fields = [
        'name', 'description', 'areas', 'categories', 'owner'
    ]

    facets = {
        'areas': TermsFacet(field='areas'),
        'categories': TermsFacet(field='categories'),
    }
