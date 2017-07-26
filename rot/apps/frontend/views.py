# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from elasticsearch_dsl import Search
from formtools.wizard.views import SessionWizardView

from frontend.forms import (
    AddItemForm1,
    AddItemForm2,
    AddItemForm3,
    AddItemForm4,
    SearchForm,
)
from register.models import Item
from search.indexes import ItemSearch


class ItemListView(TemplateView):

    template_name = "frontend/item/list.html"
    paginate_by = 20

    def post(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        form = SearchForm(self.request.POST or None)
        if form.is_valid():
            # TODO - make this search return faceted results
            search_response = ItemSearch()
            items = search_response.hits
        else:
            items = Item.objects.all()\
                .select_related('owner')\
                .prefetch_related('areas', 'categories')

        paginator = Paginator(items, self.paginate_by)

        try:
            items = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            raise Http404('Page does not exist')

        return self.render_to_response(
            self.get_context_data(items=items, form=form))


class AddItemWizard(SessionWizardView):
    """
    Form Wizard to add a new item

    see https://github.com/django/django-formtools/
    """
    form_list = [AddItemForm1, AddItemForm2, AddItemForm3, AddItemForm4]

    def done(self, form_list, **kwargs):
        return render_to_response('frontend/item/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
