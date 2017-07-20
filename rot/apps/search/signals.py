# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from register.models import Item
from search.indexes import ItemIndex


@receiver(pre_save, sender=Item, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    ItemIndex.index(instance)


@receiver(post_delete, sender=Item, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    ItemIndex.delete(instance)
