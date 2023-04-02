from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from my_game_list.my_game_list.models import BaseModel


class Friendship(BaseModel):
    """A model representing the friendship relations of the users."""

    from my_game_list.friendships.managers.friendship import FriendshipManager

    created_at = models.DateTimeField(_("creation time"), auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="_friends")

    objects = FriendshipManager()

    class Meta(BaseModel.Meta):
        verbose_name = _("friendship")
        verbose_name_plural = _("friendships")
        constraints = (models.UniqueConstraint(fields=("user", "friend"), name="unique_user_friend"),)

    def __str__(self):
        return f"User: {self.user.username}, Friend: {self.friend.username}"

    def save(self, *args, **kwargs):
        if self.user == self.friend:
            raise ValidationError(_("The user cannot befriend himself."))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = self.user
        friend = self.friend
        Friendship.objects.filter(user__in=(user, friend), friend__in=(friend, user)).delete()

        return True
