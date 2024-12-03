from django_filters.rest_framework import FilterSet
from django.utils.translation import gettext_lazy as _
from iam.models import User

class UserFilter(FilterSet):

    class Meta:
        model = User
        fields = {
            'id': ['exact'],
            'email': ['exact'],
            'username': ['exact'],
        }
