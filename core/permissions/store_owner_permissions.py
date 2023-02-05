from rest_framework import permissions
from core.choices.model_choices import RoleChoices



class WebSiteOwnerPermission(permissions.IsAuthenticated):
    """
    Permiso para vistas donde solo el store owner puede hacer una request
    """
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            return False

        return request.user.role == RoleChoices.STORE_OWNER

class WebSiteOperatorPermission(permissions.IsAuthenticated):
    """
    Permiso para vistas donde solo los operadores de la tienda matriz puede hacer una request
    """
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if not has_permission:
            return False
        if not request.user.store:
            return False
        
        return request.user.store.user_set.all().filter(role=RoleChoices.WEBSITE_OWNER).exists()
