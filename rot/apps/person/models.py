# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class Person(AbstractUser):
    role = models.CharField(max_length=100, null=True, blank=True)
    peoplefinder = models.URLField(null=True, blank=True)
    airtable_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ['last_name']
