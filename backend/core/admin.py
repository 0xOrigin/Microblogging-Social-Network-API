from django.contrib import admin
from django.conf import settings
from django.utils import timezone


class BaseAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ('id',)
    ordering = ['-id']
    list_per_page = settings.PAGINATION_ADMIN_PAGE_SIZE

    def set_audit_fields(self, request, obj, audit_by_field, audit_at_field):
        if hasattr(obj, audit_by_field):
            setattr(obj, audit_by_field, request.user)
        if hasattr(obj, audit_at_field):
            setattr(obj, audit_at_field, timezone.now())

    def save_model(self, request, obj, form, change):
        if not change:
            self.set_audit_fields(request, obj, 'created_by', 'created_at')
        else:
            self.set_audit_fields(request, obj, 'updated_by', 'updated_at')
        obj.save()


class BaseAuditTimeAdmin(BaseAdmin):
    audit_time_fields = ('created_at', 'updated_at')
    readonly_fields = BaseAdmin.readonly_fields + audit_time_fields
    list_filter = BaseAdmin.list_filter + audit_time_fields


class BaseAuditUserAdmin(BaseAdmin):
    audit_user_fields = ('created_by', 'updated_by')
    readonly_fields = BaseAdmin.readonly_fields + audit_user_fields


class BaseAuditTimeUserAdmin(BaseAuditTimeAdmin, BaseAuditUserAdmin):
    audit_fields = BaseAuditTimeAdmin.audit_time_fields + BaseAuditUserAdmin.audit_user_fields
    readonly_fields = BaseAdmin.readonly_fields + audit_fields


class BaseAuditAdmin(BaseAuditTimeUserAdmin):
    pass