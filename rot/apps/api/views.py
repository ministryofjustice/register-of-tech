# -*- coding: utf-8 -*-
from rest_framework import viewsets

from api.serializers import (
    CategoryListSerializer, ItemSerializer, BusinessAreaListSerializer,
    PeopleSerializer, ItemListSerializer, CategorySerializer,
    BusinessAreaSerializer)
from person.models import Person
from register.models import Category, Item, BusinessArea


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
