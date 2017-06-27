# -*- coding: utf-8 -*-
from rest_framework.permissions import DjangoObjectPermissions


class DjangoObjectPermissionsAnonReadOnly(DjangoObjectPermissions):
    authenticated_users_only = False

    def has_permission(self, request, view):
        if request.method not in ['GET', 'HEAD', 'OPTIONS'] and \
                not request.user.is_authenticated():
            return False
        
        return super().has_permission(request, view) or \
               self.has_object_permission(request, view, view.get_object())
