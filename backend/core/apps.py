from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        from django_filters.rest_framework import FilterSet
        from core.fields import ULIDField
        from core.filters import ULIDFilter

        FilterSet.FILTER_DEFAULTS.update({
            ULIDField: {'filter_class': ULIDFilter},
        })
