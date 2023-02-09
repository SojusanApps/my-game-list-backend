from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    The request is authenticated as a admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or super().has_permission(request, view)
        )
