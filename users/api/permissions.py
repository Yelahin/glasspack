from rest_framework import permissions 
    
class IsAdminUserOrUnauthorizedUserOnlyCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user and request.user.is_staff:
                return True
            return not bool(request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)
    