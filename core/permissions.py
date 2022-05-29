from rest_framework import permissions




class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff == True:
            return True
        return obj == request.user