"""This module contains the viewsets for the friendship related data."""

from typing import TYPE_CHECKING, Self

from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from my_game_list.friendships.filters import (
    FriendshipFilterSet,
    FriendshipRequestFilterSet,
)
from my_game_list.friendships.models import Friendship, FriendshipRequest
from my_game_list.friendships.serializers import (
    FriendshipRequestCreateSerializer,
    FriendshipRequestSerializer,
    FriendshipSerializer,
)
from my_game_list.notifications.constants import NotificationCategory, NotificationVerb
from my_game_list.notifications.utils import notify_send

if TYPE_CHECKING:
    from rest_framework.request import Request


User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        description=(
            "List confirmed friendships for the authenticated user. "
            "A Friendship is a bidirectional, established relationship. "
            "Each record represents one direction of the relationship."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact friendship record ID.",
            ),
            OpenApiParameter(
                name="user",
                description="Filter by user ID.",
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve a single friendship record by ID.",
    ),
    destroy=extend_schema(
        description=(
            "Remove a friendship. This action is unilateral: only the authenticated user's "
            "friendship record is deleted. The other party retains their record until they "
            "also remove the friendship."
        ),
    ),
)
class FriendshipViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet["Friendship"]):
    """All views related to friendship."""

    queryset = Friendship.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FriendshipSerializer
    filterset_class = FriendshipFilterSet


@extend_schema_view(
    list=extend_schema(
        description=(
            "List friendship requests. "
            "Returns requests sent by or directed to authenticated users. "
            "Use the `sender` and `receiver` filters to narrow results."
        ),
        parameters=[
            OpenApiParameter(
                name="id",
                description="Filter by exact friendship request ID.",
            ),
            OpenApiParameter(
                name="sender",
                description="Filter by the user ID who sent the request.",
            ),
            OpenApiParameter(
                name="receiver",
                description="Filter by the user ID who received the request.",
            ),
        ],
    ),
    create=extend_schema(
        description="Send a friendship request to another user. A notification is sent to the recipient.",
    ),
    retrieve=extend_schema(
        description="Retrieve a single friendship request by ID.",
    ),
    destroy=extend_schema(
        description="Cancel a friendship request before it is accepted or rejected.",
    ),
)
class FriendshipRequestViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet["FriendshipRequest"],
):
    """All views related to friendship requests."""

    queryset = FriendshipRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = FriendshipRequestFilterSet

    def get_serializer_class(
        self: Self,
    ) -> type[FriendshipRequestCreateSerializer | FriendshipRequestSerializer]:
        """Get the serializer class for the request."""
        return FriendshipRequestCreateSerializer if self.action == "create" else FriendshipRequestSerializer

    def perform_create(self: Self, serializer: serializers.BaseSerializer[FriendshipRequest]) -> None:
        """Create a friendship request and send a notification."""
        user = self.request.user
        if not user.is_authenticated:
            return
        instance = serializer.save(sender=user)
        notify_send(
            sender=user,
            recipient=instance.receiver,
            verb=NotificationVerb.FRIEND_REQUEST_SENT,
            category=NotificationCategory.FRIENDSHIP,
        )

    @extend_schema(
        description=(
            "Accept a pending friendship request. "
            "Creates reciprocal Friendship records for both the sender and receiver, "
            "and sends a notification to the original sender confirming the acceptance."
        ),
        request=None,
        responses={204: None},
    )
    @action(detail=True, methods=("post",))
    def accept(self: Self, request: Request, pk: int) -> Response:  # noqa: ARG002
        """Accept a friendship request."""
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        instance: FriendshipRequest = self.get_object()
        instance.accept()

        notify_send(
            sender=user,
            recipient=instance.sender,
            verb=NotificationVerb.FRIEND_REQUEST_ACCEPTED,
            category=NotificationCategory.FRIENDSHIP,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description=(
            "Reject a pending friendship request. "
            "The request record is deleted. No notification is sent to the requester."
        ),
        request=None,
        responses={204: None},
    )
    @action(detail=True, methods=("post",))
    def reject(self: Self, request: Request, pk: int) -> Response:  # noqa: ARG002
        """Reject a friendship request."""
        instance: FriendshipRequest = self.get_object()
        instance.reject()

        return Response(status=status.HTTP_204_NO_CONTENT)
