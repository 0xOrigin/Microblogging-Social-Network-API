from rest_framework.permissions import DjangoModelPermissions


class BasePermissions(DjangoModelPermissions):

    def has_permission(self, request, view):
        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
