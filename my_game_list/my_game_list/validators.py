from typing import Any

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_size(value: Any) -> None:
    """File size validator."""
    limit = settings.LIMIT_AVATAR_SIZE
    if value.size > limit:
        raise ValidationError(
            _("File too large. Size should not exceed {limit} B").format(limit=limit)
        )
