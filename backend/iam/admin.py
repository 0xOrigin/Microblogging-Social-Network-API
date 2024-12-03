from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.utils import dynamic_admin_readonly_fields
from core.admin import BaseAuditAdmin
from iam.models import User


@admin.register(User)
class UserAdmin(BaseAuditAdmin, BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'last_login',)
    search_fields = ('username', 'email')
    readonly_fields = dynamic_admin_readonly_fields(User, extra_fields=['last_login', 'date_joined'])
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email')}),
        ('Permissions', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates & logs', {
                'fields': ('last_login', 'date_joined', 'created_at', 'updated_at', 'created_by', 'updated_by',),
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            },
        ),
    )
    exclude = ()

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    actions = ['activate_selected_users', 'deactivate_selected_users']

    def activate_selected_users(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_selected_users(self, request, queryset):
        queryset.update(is_active=False)
