# -*- coding: utf-8 -*-
from django import forms

from person.models import Person
from register.models import Category, BusinessArea


class AddItemForm1(forms.Form):
    """
    Form for adding categories to an Item
    First form to be used in AddItemWizard view from views
    see https://github.com/django/django-formtools/
    """
    categories = forms.ModelChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
    )


class AddItemForm2(forms.Form):
    """
    Form for adding areas to an Item
    """
    areas = forms.ModelChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        queryset=BusinessArea.objects.all(),
    )


class AddItemForm3(forms.Form):
    """
    Form for addin name and description to an item
    """
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)


class AddItemForm4(forms.Form):
    """
    Form for adding an owner to an Item
    """
    # TODO - this will need some way of creating a Person if that person
    # doesn't exist in the DB
    owner = forms.ModelChoiceField(
        required=True,
        queryset=Person.objects.all(),
    )


class SearchForm(forms.Form):
    """Search Form"""
    SORT_CHOICES = (
        ('name.raw', 'Name (asc)'),
        ('-name.raw', 'Name (desc)'),
        ('owner.raw', 'Owner (asc)'),
        ('-owner.raw', 'Owner (desc)'),
    )
    search = forms.CharField(max_length=100, required=False)
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False)
    category = forms.CharField(max_length=100, required=False)
