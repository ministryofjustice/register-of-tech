# -*- coding: utf-8 -*-
from django.conf.urls import url

from frontend.views import ItemListView, ItemDetailView


urlpatterns = [
    url(r'^services$', ItemListView.as_view(), name='services-list'),
    url(r'^services/(?P<pk>[-\d]+)/$', ItemDetailView.as_view(),
        name='services-detail'),
]
