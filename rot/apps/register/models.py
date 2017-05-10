# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField

from mptt.models import MPTTModel, TreeForeignKey

from register.constants import RELATIONSHIPS


class TimestampedUserModelMixin:
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='items_created', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Type(MPTTModel, TimestampedUserModelMixin):
    """
    Type of Item in list - Software, API, etc.
    Allows for nesting of types i.e. API could be nested within Software
    
    Defines schema for all items that relate to this type
    
    Schema format is tbd but could possibly use Django Rest Framework field 
    types for validation.
    
    Maybe something like:
    
    {
        "field_name": {
            "type": "DRFFieldType",
            "required": true
        }
    }
    
    """
    name = models.CharField(max_length=100)
    schema = JSONField()
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)


class ItemRelation(models.Model):
    """
    Through model for linked relations between Items
    
    Defines the relationship and direction and direction
    
    Allows for naming of relationship
    
    This might not be necessary...
    """
    name = models.CharField(max_length=100)
    relationship = models.PositiveIntegerField(choices=RELATIONSHIPS)
    from_obj = models.ForeignKey('Item', on_delete=models.CASCADE,
                                 related_name='from_obj')
    to_obj = models.ForeignKey('Item', on_delete=models.CASCADE,
                               related_name='to_obj')


class Item(models.Model, TimestampedUserModelMixin):
    """
    Item is the base data record.
    
    Data attributes can be stored in data json b field and must adhere to 
    the schema from the related type.
    """
    name = models.CharField(max_length=100)
    type = models.ForeignKey('Type')
    links = models.ManyToManyField(
        'self',
        through='ItemRelation',
        through_fields=('from_obj', 'to_obj'),
        symmetrical=False,
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items')
    data = JSONField()
