# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, ImproperlyConfigured
from elasticsearch_dsl import Search
from rest_framework import viewsets
from rest_framework_elasticsearch import es_views, es_filters

from api.pagination import (
    LargeResultsSetPagination,
    SmallResultsSetPagination
)
from api.serializers import (
    CategoryListSerializer,
    ItemSerializer,
    BusinessAreaListSerializer,
    PeopleSerializer,
    ItemListSerializer,
    CategorySerializer,
    BusinessAreaSerializer
)
from person.models import Person
from register.models import Category, Item, BusinessArea
from search.indexes import ItemIndex, ItemSearch
from search.pagination import ElasticPageNumberPagination


class BaseNestedModelViewSet(viewsets.ModelViewSet):
    serializers = {}

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializer_class)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(level=0)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    """
    View set for Category

    retrieve:
    Detail view of a single Category

    list:
    List view of Categorys
    
    create:
    Add new Category
    
    update:
    Update existing Category
    
    patch:
    Partially update existing Category
    
    delete:
    Delete a Category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    serializers = {
        'list': CategoryListSerializer,
    }
    pagination_class = LargeResultsSetPagination


class ItemViewSet(viewsets.ModelViewSet):
    """
    View set for Item

    retrieve:
    Detail view of a single Item

    list:
    List view of Items

    create:
    Add new Item

    update:
    Update existing Item
    
    patch:
    Partially update existing Item
    
    delete:
    Delete a Item
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    serializers = {
        'list': ItemListSerializer,
    }
    pagination_class = SmallResultsSetPagination


class BusinessAreaViewSet(viewsets.ModelViewSet):
    """
    View set for BusinessArea

    retrieve:
    Detail view of a single BusinessArea

    list:
    List view of BusinessAreas

    create:
    Add new BusinessArea

    update:
    Update existing BusinessArea

    patch:
    Partially update existing BusinessArea

    delete:
    Delete a BusinessArea
    """
    queryset = BusinessArea.objects.all()
    serializer_class = BusinessAreaSerializer
    serializers = {
        'list': BusinessAreaListSerializer,
    }
    pagination_class = LargeResultsSetPagination


class PeopleViewSet(viewsets.ModelViewSet):
    """
    View set for People

    retrieve:
    Detail view of a single Person

    list:
    List view of People

    create:
    Add new Person

    update:
    Update existing Person

    patch:
    Partially update existing Person

    delete:
    Delete a Person
    """
    queryset = Person.objects.all()
    serializer_class = PeopleSerializer
    pagination_class = LargeResultsSetPagination


class ItemSearchView(es_views.ListElasticAPIView):
    es_paginator = ElasticPageNumberPagination()
    queryset = Item.objects.all()
    es_client = Elasticsearch()
    es_model = ItemIndex
    es_filter_backends = (
        es_filters.ElasticFieldsFilter,
        es_filters.ElasticSearchFilter
    )
    es_filter_fields = (
        es_filters.ESFieldFilter('area', 'areas'),
        es_filters.ESFieldFilter('category', 'categories'),
        es_filters.ESFieldFilter('owner', 'owner'),
    )
    es_search_fields = (
        'name',
        'description',
        'owner',
        'areas',
        'categories',
    )

    def get_es_search(self):
        if self.es_model is None:
            msg = (
                "Cannot use %s on a view which does not have the 'es_model'"
            )
            raise ImproperlyConfigured(msg % self.__class__.__name__)
        index = self.es_model()._get_index()
        es_client = self.get_es_client()
        s = Search(using=es_client, index=index)

        return s
