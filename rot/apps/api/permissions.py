# -*- coding: utf-8 -*-
from rest_framework.permissions import DjangoObjectPermissions


class DjangoObjectPermissionsAnonReadOnly(DjangoObjectPermissions):
    authenticated_users_only = False
