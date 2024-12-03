from collections import OrderedDict
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.paginations import BasePagination
from core.permissions import BasePermissions
from core.renderers import BaseJSONRenderer, BaseBrowsableAPIRenderer


class BaseViewSet(viewsets.ModelViewSet):
    model = None
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = BasePagination
    permission_classes = [BasePermissions,]
    renderer_classes = [BaseJSONRenderer, BaseBrowsableAPIRenderer]

    def get_queryset(self):
        if self.model is None:
            raise NotImplementedError(_('BaseViewSet must be subclassed with a model'))
        return self.customize_queryset_filter()

    def get_current_user(self):
        return self.request.user if self.request.user.is_authenticated else None

    def get_datetime_now(self):
        return timezone.now()

    def customize_queryset_filter(self):
        return self.model.objects.all()

    def set_audit_fields(self, dict_to_store, audit_by_field, audit_at_field):
        if hasattr(self.model, audit_by_field):
            dict_to_store[audit_by_field] = self.get_current_user()
        if hasattr(self.model, audit_at_field):
            dict_to_store[audit_at_field] = self.get_datetime_now()

    def perform_create(self, serializer):
        extra_data = dict()
        self.set_audit_fields(extra_data, 'created_by', 'created_at')
        serializer.save(**extra_data)

    def perform_update(self, serializer):
        extra_data = dict()
        self.set_audit_fields(extra_data, 'updated_by', 'updated_at')
        serializer.save(**extra_data)

    def get_list_response(self, data, queryset):
        return Response({
            'meta': OrderedDict([
                ('count', queryset.count()),
            ]),
            'data': data
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.get_list_response(serializer.data, queryset)


def method_not_allowed(method):
    raise MethodNotAllowed(method=method)


class NonListableViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        return method_not_allowed(request.method)


class NonCreatableViewSet(viewsets.ModelViewSet):
    
    def create(self, request, *args, **kwargs):
        return method_not_allowed(request.method)


class NonUpdatableViewSet(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        return method_not_allowed(request.method)

    def partial_update(self, request, *args, **kwargs):
        return method_not_allowed(request.method)


class NonDeletableViewSet(viewsets.ModelViewSet):

    def destroy(self, request, *args, **kwargs):
        return method_not_allowed(request.method)
