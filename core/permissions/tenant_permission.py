from rest_framework.exceptions import ValidationError
from rest_framework import permissions

class ViewActions:
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    RETRIEVE = "retrieve"
    PARTIAL = "partial_update"
    DELETE = "delete"

def get_tenant_from_request(request):
    pass

class TenantPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):

        if view.action in [ViewActions.CREATE, ViewActions.UPDATE, ViewActions.PARTIAL] and not request.user:
            raise ValidationError("No posee un Tenant asignado a su usuario para ingresar productos, por favor contactese con soporte")
        
        return super().has_permission(request, view)
    def has_object_permission(self, request, view, obj):
        if view.action in [ViewActions.RETRIEVE, ViewActions.LIST]:
            return True
        if request.user.store != obj.store:
            return False
        return super().has_object_permission(request, view, obj)