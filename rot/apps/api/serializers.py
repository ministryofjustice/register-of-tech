# -*- coding: utf-8 -*-
from rest_framework import serializers

from register.models import Type


class BaseItemSerializer(serializers.ModelSerializer):
    pass


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
