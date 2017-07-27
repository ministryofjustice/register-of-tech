# -*- coding: utf-8 -*-
from django.conf.urls import url

from frontend.views import ItemListView


urlpatterns = [
    url(r'^services$', ItemListView.as_view(), name='services-list')
]
