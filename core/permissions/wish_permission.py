from rest_framework import permissions




class SameUserPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if not request.user == obj.user:
            return False
        return super().has_object_permission(request, view, obj)