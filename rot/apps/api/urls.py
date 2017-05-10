# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from api.views import TypeViewSet

schema_view = get_swagger_view(title='Register of Things')

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'types', TypeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('django_gov.urls')),
    url(r'^docs', schema_view, name='api-docs'),
]
