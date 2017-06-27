# -*- coding: utf-8 -*-
from rest_framework import serializers

from person.models import Person
from register.models import Category, Item, BusinessArea


class BaseItemSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_id']


class CategoryListSerializer(CategorySerializer):
    children = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = CategoryListSerializer(obj.children.all(), many=True)
        return serializer.data

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['children']


class BusinessAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessArea
        fields = ['id', 'name', 'description', 'parent_id']


class BusinessAreaListSerializer(BusinessAreaSerializer):
    children = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = BusinessAreaListSerializer(obj.children.all(), many=True)
        return serializer.data

    class Meta(BusinessAreaSerializer.Meta):
        fields = BusinessAreaSerializer.Meta.fields + ['children']


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'email', 'role',
                  'peoplefinder']


class ItemSerializer(BaseItemSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category_id', 'area_id', 'owner_id']


class ItemListSerializer(BaseItemSerializer):
    owner = PeopleSerializer(many=False)
    category = CategorySerializer(many=False)
    area = BusinessAreaSerializer(many=False)
