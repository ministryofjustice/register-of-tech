# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from api.views import (
    CategoryViewSet, ItemViewSet, BusinessAreaViewSet, PeopleViewSet)

schema_view = get_swagger_view(title='Register of Things')

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'items', ItemViewSet, base_name='item')
router.register(r'areas', BusinessAreaViewSet, base_name='area')
router.register(r'people', PeopleViewSet, base_name='people')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('django_gov.urls')),
    url(r'^docs', schema_view, name='api-docs'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
