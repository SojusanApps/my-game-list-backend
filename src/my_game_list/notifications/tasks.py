"""Tasks for the notifications app."""

import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from my_game_list.notifications.models import Notification

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_notifications() -> None:
    """
    Delete old notifications.

    Read notifications older than 14 days and unread notifications older than 30 days.
    """
    now = timezone.now()
    read_cutoff = now - timedelta(days=14)
    unread_cutoff = now - timedelta(days=30)

    # Delete read notifications older than 14 days
    read_deleted_count, _ = Notification.objects.filter(unread=False, timestamp__lt=read_cutoff).delete()

    # Delete unread notifications older than 30 days
    unread_deleted_count, _ = Notification.objects.filter(unread=True, timestamp__lt=unread_cutoff).delete()

    logger.info(
        "Notification cleanup task finished. Deleted %d read and %d unread notifications.",
        read_deleted_count,
        unread_deleted_count,
    )
