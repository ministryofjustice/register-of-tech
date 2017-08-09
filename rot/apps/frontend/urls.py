# -*- coding: utf-8 -*-
from django.conf.urls import url

from frontend.views import ItemListView, ItemDetailView, AddItemWizard

urlpatterns = [
    url(r'^services$', ItemListView.as_view(), name='services-list'),
    url(r'^services/new/$', AddItemWizard.as_view(), name='services-create'),
    url(r'^services/(?P<slug>[-\w\d]+)/$', ItemDetailView.as_view(),
        name='services-detail'),
]


