"""Views for the notifications app."""

from typing import TYPE_CHECKING, Self

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import IntegerField
from rest_framework.viewsets import GenericViewSet

from my_game_list.notifications.filters import NotificationFilterSet
from my_game_list.notifications.models import Notification
from my_game_list.notifications.serializers import NotificationSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request

    from my_game_list.notifications.models import NotificationQuerySet


class NotificationViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet[Notification]):
    """ViewSet for handling notifications."""

    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = NotificationFilterSet

    def get_queryset(self: Self) -> NotificationQuerySet:
        """Get the queryset for the current user."""
        user = self.request.user
        if not user.is_authenticated:
            return Notification.objects.none()
        return Notification.objects.filter(recipient=user)

    @extend_schema(
        responses={
            200: inline_serializer(
                name="UnreadCountResponse",
                fields={"unread_count": IntegerField(help_text="The count of unread notifications.")},
            ),
        },
    )
    @action(detail=False, methods=("get",))
    def unread_count(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Get the count of unread notifications."""
        count = self.get_queryset().unread().count()
        return Response({"unread_count": count})

    @extend_schema(
        request=None,
        responses={204: None},
    )
    @action(detail=True, methods=("post",))
    def mark_as_read(self: Self, request: Request, pk: int) -> Response:  # noqa: ARG002
        """Mark a specific notification as read."""
        instance = self.get_object()
        instance.mark_as_read()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={204: None},
    )
    @action(detail=False, methods=("post",))
    def mark_all_as_read(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Mark all notifications as read for the user."""
        self.get_queryset().unread().mark_all_as_read()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={204: None},
    )
    @action(detail=False, methods=("delete",))
    def delete_all_read(self: Self, request: Request) -> Response:  # noqa: ARG002
        """Delete all read notifications for the user."""
        self.get_queryset().filter(unread=False).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
