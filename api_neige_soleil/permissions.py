from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
    	return (request.user.id == int(request.data["user"]) or request.user.is_superuser)