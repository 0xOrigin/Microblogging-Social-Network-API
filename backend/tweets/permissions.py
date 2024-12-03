from core.permissions import BasePermissions


class TweetPermissions(BasePermissions):
    
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)

        if view.action in ['list', 'retrieve']:
            return True

        return has_permission

    def has_object_permission(self, request, view, obj):
        user = request.user

        if view.action in ['list', 'retrieve']:
            return True

        if view.action == 'create':
            return user.is_authenticated

        return obj.created_by.pk == user.pk
