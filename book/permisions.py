from pickle import OBJ
from urllib import request
from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True

            is_staff = request.user.is_staff == True
            return is_staff
