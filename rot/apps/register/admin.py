# -*- coding: utf-8 -*-
from django.contrib import admin

from register.models import Item, Category, BusinessArea


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(BusinessArea)
