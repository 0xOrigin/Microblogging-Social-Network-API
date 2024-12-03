from django.apps import AppConfig


class IamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iam'

    def ready(self):
        import iam.signals.handlers
