from rest_framework import permissions

def is_super_admin(user):
    return (user.is_authenticated and 
            user.main_role is not None and 
            user.main_role.name.lower() == 'superadmin')

class IsSuperAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_super_admin(request.user)

class IsUniversityAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.main_role is None:
            return False
        
        role_name = user.main_role.name.lower()
        
        if role_name == 'superadmin':
            return True
            
        return (role_name == 'admin' and user.university is not None)

class IsSectionStaffRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.main_role is None:
            return False
        
        role_name = user.main_role.name.lower()
        allowed_roles = ['superadmin', 'admin', 'teacher']
        
        return role_name in allowed_roles