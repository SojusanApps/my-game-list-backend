"""This module contains the custom permission classes for collections."""

from typing import TYPE_CHECKING, Self

from rest_framework import permissions

from my_game_list.collections.models import Collection, CollectionItem, CollectionMode, CollectionVisibility
from my_game_list.friendships.models import Friendship

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.views import APIView


class IsCollectionOwner(permissions.BasePermission):
    """Permission to check if user is the collection owner."""

    def has_object_permission(self: Self, request: Request, view: APIView, obj: Collection) -> bool:  # noqa: ARG002
        """Check if user is the owner of the collection."""
        return obj.user == request.user


class IsCollectionOwnerOrCollaborator(permissions.BasePermission):
    """Permission to check if user is owner or collaborator of a collection."""

    def has_object_permission(self: Self, request: Request, view: APIView, obj: Collection) -> bool:  # noqa: ARG002
        """Check if user is owner or collaborator."""
        if not request.user.is_authenticated or request.user.id is None:
            return False

        if obj.user == request.user:
            return True
        if obj.mode == CollectionMode.COLLABORATIVE:
            return obj.collaborators.filter(id=request.user.id).exists()
        return False


class CanViewCollection(permissions.BasePermission):
    """Permission to check if user can view a collection based on visibility."""

    def has_object_permission(self: Self, request: Request, view: APIView, obj: Collection) -> bool:  # noqa: ARG002
        """Check if user can view the collection based on visibility settings."""
        if not request.user.is_authenticated or request.user.id is None:
            return False

        # Owner can always view
        if obj.user == request.user:
            return True

        # Collaborators can always view
        if obj.collaborators.filter(id=request.user.id).exists():
            return True

        # Check visibility
        if obj.visibility == CollectionVisibility.PUBLIC:
            return True

        if obj.visibility == CollectionVisibility.FRIENDS:
            # Check if user is a friend of the owner
            return Friendship.objects.filter(user=obj.user, friend=request.user).exists()

        # PRIVATE - only owner and collaborators (already checked above)
        return False


class CollectionPermission(permissions.BasePermission):
    """Combined permission class for collection operations.

    - List: Only own collections + visible collections based on visibility
    - Create: Any authenticated user
    - Retrieve: Based on visibility settings
    - Update/Delete: Only owner
    """

    def has_permission(self: Self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        """Check basic permission - user must be authenticated."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self: Self, request: Request, view: APIView, obj: Collection) -> bool:  # noqa: ARG002
        """Check object-level permissions."""
        if not request.user.is_authenticated or request.user.id is None:
            return False

        # Owner can do anything
        if obj.user == request.user:
            return True

        # For safe methods (GET, HEAD, OPTIONS), check visibility
        if request.method in permissions.SAFE_METHODS:
            # Collaborators can always view
            if obj.collaborators.filter(id=request.user.id).exists():
                return True

            if obj.visibility == CollectionVisibility.PUBLIC:
                return True

            if obj.visibility == CollectionVisibility.FRIENDS:
                return Friendship.objects.filter(user=obj.user, friend=request.user).exists()

        # For unsafe methods (PUT, PATCH, DELETE), only owner allowed
        return False


class CollectionItemPermission(permissions.BasePermission):
    """Permission class for collection item operations.

    - List: Filter by collection visibility
    - Create: Owner or collaborator (if COLLABORATIVE mode)
    - Update/Delete: Owner or collaborator (if COLLABORATIVE mode)
    """

    def has_permission(self: Self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        """Check basic permission - user must be authenticated."""
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self: Self, request: Request, view: APIView, obj: CollectionItem) -> bool:  # noqa: ARG002
        """Check object-level permissions for collection item."""
        if not request.user.is_authenticated or request.user.id is None:
            return False

        collection = obj.collection

        # Collection owner can do anything
        if collection.user == request.user:
            return True

        # Check if user is a collaborator
        is_collaborator = collection.collaborators.filter(id=request.user.id).exists()

        # For safe methods, check visibility
        if request.method in permissions.SAFE_METHODS:
            if is_collaborator or collection.visibility == CollectionVisibility.PUBLIC:
                return True

            if collection.visibility == CollectionVisibility.FRIENDS:
                return Friendship.objects.filter(user=collection.user, friend=request.user).exists()

            return False

        # For unsafe methods, must be owner or collaborator in COLLABORATIVE mode
        return collection.mode == CollectionMode.COLLABORATIVE and is_collaborator
