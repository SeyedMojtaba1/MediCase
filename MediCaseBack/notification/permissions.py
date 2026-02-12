from rest_framework import permissions

def is_super_admin(user):
    return (user.is_authenticated and 
            user.main_role is not None and 
            user.main_role.name == 'SuperAdmin')

class IsSuperAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_super_admin(request.user)

class IsUniversityAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.main_role is None:
            return False
        
        if user.main_role.name == 'SuperAdmin':
            return True
            
        return (user.main_role.name == 'Admin' and user.university is not None)

# --- کلاس جدید برای چک کردن سطح دسترسی سکشن ---
class IsSectionStaffRole(permissions.BasePermission):
    """
    اجازه دسترسی به کسانی که نقش‌های مدیریتی یا آموزشی دارند:
    1. SuperAdmin
    2. Admin
    3. Teacher
    (دانشجویان اجازه ایجاد/ویرایش ندارند)
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.main_role is None:
            return False
        
        allowed_roles = ['SuperAdmin', 'Admin', 'Teacher']
        return user.main_role.name in allowed_roles