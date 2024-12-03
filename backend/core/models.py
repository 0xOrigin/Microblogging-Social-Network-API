from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.fields import new_ulid, ULIDField


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(models.Manager):

    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)


class BaseModel(models.Model):
    id = ULIDField(primary_key=True, default=new_ulid, editable=False)

    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


class BaseAuditTimeModel(BaseModel):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class BaseAuditUserModel(BaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated_by')

    class Meta:
        abstract = True


class BaseAuditTimeUserModel(BaseAuditTimeModel, BaseAuditUserModel):

    class Meta:
        abstract = True


class BaseAuditModel(BaseAuditTimeUserModel):

    class Meta:
        abstract = True
