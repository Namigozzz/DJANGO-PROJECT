from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
