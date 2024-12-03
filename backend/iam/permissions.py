from core.permissions import BasePermissions


class UserPermissions(BasePermissions):

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        user = request.user

        if view.action == 'list':
            return has_permission and user.is_superuser
        
        return has_permission
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if view.action == 'retrieve':
            return True

        return obj.pk == user.pk


class FollowPermissions(BasePermissions):

    def has_object_permission(self, request, view, obj):
        return obj.follower.pk == request.user.pk
