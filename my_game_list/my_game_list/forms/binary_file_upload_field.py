"""BinaryField with option to upload files by admin panel."""
from base64 import b64encode
from typing import Any, Self

from django.core.files import File
from django.forms import FileField


class BinaryFieldWithUpload(FileField):
    """Allows to upload image to the field via admin panel."""

    def to_python(self: Self, data: File[Any] | None) -> str:  # type: ignore[override]
        """Return the decoded value."""
        data = super().to_python(data)
        if data:
            data = b64encode(data.read()).decode("utf-8")  # type: ignore[assignment]
        return data  # type: ignore[return-value]
