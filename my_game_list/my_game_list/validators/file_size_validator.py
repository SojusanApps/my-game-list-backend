"""The validator for size of the file in the file field."""

from typing import Self

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _


class FileSizeValidator(BaseValidator):
    """The validator for size of the file in the file field."""

    message = _("File too large. Size cannot exceed {limit} KB.")
    code = "file_too_large"

    def __init__(self: Self) -> None:
        """The init function for FileSizeValidator."""

    def __call__(self: Self, value: FieldFile) -> None:
        """The file size validator."""
        limit = settings.LIMIT_FILE_SIZE
        if value.size > limit:
            bytes_to_kilobytes = limit / 1024
            raise ValidationError(self.message.format(limit=bytes_to_kilobytes))
