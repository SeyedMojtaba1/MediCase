from rest_framework import permissions

class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.main_role and request.user.main_role.name in ['superadmin']:
            return True
            
        return False