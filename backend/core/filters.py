from django_filters.rest_framework import filters, FilterSet
from core import forms


class ULIDFilter(filters.Filter):
    field_class = forms.ULIDField
