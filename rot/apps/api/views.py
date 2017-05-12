# -*- coding: utf-8 -*-
from rest_framework import viewsets

from api.serializers import CategorySerializer, ItemSerializer
from register.models import Category, Item


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
    Partially update existing Type
    
    delete:
    Delete a Type
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
