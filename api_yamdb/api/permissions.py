from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )
