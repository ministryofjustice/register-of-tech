# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
from django_extensions.db.fields import AutoSlugField

from mptt.models import MPTTModel, TreeForeignKey

from register.constants import RELATIONSHIPS


class TimestampedUserModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(app_label)s_%(class)s_created',
        null=True,
        blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


DEFAULT_SCHEMA = {}


class Category(MPTTModel, TimestampedUserModel):
    """
    Category of Item in list - Software, API, etc.
    Allows for nesting of Categorys i.e. API could be nested within Software
    
    Defines schema for all items that relate to this Category
    
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
    schema = JSONField(default=DEFAULT_SCHEMA)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    airtable_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemRelation(TimestampedUserModel):
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


class Item(TimestampedUserModel):
    """
    Item is the base data record.
    
    Data attributes can be stored in data json b field and must adhere to 
    the schema from the related Category.
    """
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    description = models.TextField(null=True)
    categories = models.ManyToManyField('Category')
    areas = models.ManyToManyField('BusinessArea')
    links = models.ManyToManyField(
        'self',
        through='ItemRelation',
        through_fields=('from_obj', 'to_obj'),
        symmetrical=False,
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items')
    data = JSONField(default={})
    airtable_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['name']


class BusinessArea(MPTTModel, TimestampedUserModel):
    """
    Business Area
    
    Nested model to allow for sub areas
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    airtable_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
