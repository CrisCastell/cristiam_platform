from rest_framework import permissions

class IsAssigned(permissions.BasePermission): 
    
    def has_object_permission(self, request, view, obj):
		# check if user who launched request is object owner 
        if obj.author == request.user: 
            return True
        else:
            return False