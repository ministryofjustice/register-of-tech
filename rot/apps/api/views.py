# -*- coding: utf-8 -*-
from rest_framework import viewsets

from api.serializers import TypeSerializer
from register.models import Type


class TypeViewSet(viewsets.ModelViewSet):
    """
    View set for type

    retrieve:
    Detail view of a single type

    list:
    List view of types
    
    add:
    Add new type
    
    update:
    Update existing type
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
