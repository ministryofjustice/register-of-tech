# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm

from register.models import Item


def all_perms(user, obj, func=assign_perm):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    all_permissions = Permission.objects.filter(content_type=content_type)
    for perm in all_permissions:
        func(perm.codename, user, obj)


@receiver(pre_save, sender=Item)
def user_post_save(sender, instance, **kwargs):
    if instance.created_by:
        all_perms(instance.created_by, instance, func=remove_perm)
    if instance.owner:
        all_perms(instance.owner, instance, func=remove_perm)


@receiver(post_save, sender=Item)
def user_post_save(sender, instance, **kwargs):
    if instance.created_by:
        all_perms(instance.created_by, instance)
    if instance.owner:
        all_perms(instance.owner, instance)
