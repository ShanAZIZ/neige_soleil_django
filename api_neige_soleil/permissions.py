from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
	# TODO: Permission ne fonctionne pas
    def has_permission(self, request, view):
    	if request.data["user"]:
    		return request.user.id == int(request.data["user"]) 
    	return request.user.is_superuser