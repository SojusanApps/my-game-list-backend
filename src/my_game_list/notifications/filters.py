"""Filters for the notifications app."""

from django_filters import rest_framework as filters

from my_game_list.notifications.models import Notification


class NotificationFilterSet(filters.FilterSet):
    """FilterSet for the Notification model."""

    category = filters.ChoiceFilter(choices=Notification.CATEGORY_CHOICES)
    level = filters.ChoiceFilter(choices=Notification.LEVEL_CHOICES)
    unread = filters.BooleanFilter()

    class Meta:
        """Meta data for NotificationFilterSet."""

        model = Notification
        fields = (
            "category",
            "level",
            "unread",
        )
