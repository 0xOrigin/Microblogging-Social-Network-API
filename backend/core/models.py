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


class BaseAuditCreateModel(BaseModel):
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created_by')

    class Meta:
        abstract = True


class BaseAuditUpdateModel(BaseModel):
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated_by')
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class BaseAuditModel(BaseAuditCreateModel, BaseAuditUpdateModel):

    class Meta:
        abstract = True
