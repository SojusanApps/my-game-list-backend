from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from my_game_list.friendships.models import FriendshipRequest
from my_game_list.friendships.serializers import FriendshipRequestCreateSerializer, FriendshipRequestSerializer

User = get_user_model()


class FriendshipRequestViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """All views related to friendship requests."""

    queryset = FriendshipRequest.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return FriendshipRequestCreateSerializer if self.action == "create" else FriendshipRequestSerializer

    @action(detail=True, methods=("post",))
    def accept(self, request: Request, pk: int) -> Response:
        """Accept a friendship request."""
        instance: FriendshipRequest = self.get_object()
        instance.accept()

        return Response({"detail": _("Success")}, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post",),
    )
    def reject(self, request: Request, pk: int) -> Response:
        """Reject a friendship request."""
        instance: FriendshipRequest = self.get_object()
        instance.reject()

        return Response({"detail": _("Success")}, status=status.HTTP_200_OK)
