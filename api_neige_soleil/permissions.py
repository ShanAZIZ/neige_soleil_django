from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
	# TODO: Browsable ne fonctionne pas avec la IsAdminOrOwner 
    def has_permission(self, request, view):
    	if request.data["user"]:
    		return request.user.id == int(request.data["user"]) 
    	return request.user.is_superuser