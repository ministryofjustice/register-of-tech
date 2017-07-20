# -*- coding: utf-8 -*-
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer

from register.models import Item
from search.indexes import ItemIndex


class ElasticItemSerializer(ElasticModelSerializer):
    class Meta:
        model = Item
        es_model = ItemIndex
        fields = (
            'pk', 'name', 'description', 'areas', 'categories', 'created',
            'modified'
        )
