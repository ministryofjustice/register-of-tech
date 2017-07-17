# -*- coding: utf-8 -*-
from haystack import indexes
from register.models import Item


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    def get_model(self):
        return Item
