from rest_framework import permissions

class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.main_role and request.user.main_role.name in ['superadmin', 'admin']:
            return True
            
        return False