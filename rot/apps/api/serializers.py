# -*- coding: utf-8 -*-
from rest_framework import serializers

from person.models import Person
from register.models import Category, Item, BusinessArea


class BaseItemSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class NestedCategorySerializer(CategorySerializer):
    children = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = NestedCategorySerializer(obj.children.all(), many=True)
        return serializer.data

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['children']


class BusinessAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessArea
        fields = ['id', 'name', 'description']


class NestedBusinessAreaSerializer(BusinessAreaSerializer):
    children = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = NestedBusinessAreaSerializer(obj.children.all(), many=True)
        return serializer.data

    class Meta(BusinessAreaSerializer.Meta):
        fields = BusinessAreaSerializer.Meta.fields + ['children']


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'email', 'role',
                  'peoplefinder']


class ItemSerializer(BaseItemSerializer):
    owner = PeopleSerializer(many=False)
    category = CategorySerializer(many=False)
    area = BusinessAreaSerializer(many=False)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'area', 'owner']

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
