from rest_framework import permissions

# This enables it such that only owners of the snippets can edit or delete them.
class IsOwnerOrReadOnly(permissions.BasePermission):
    
    # Overriding the inherited function. Allow GET, HEAD or OPTIONS request only
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user