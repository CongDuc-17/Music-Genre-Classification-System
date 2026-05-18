from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_audio_extension(value) -> None:
    name = getattr(value, "name", "") or ""
    ext = Path(name).suffix.lower()
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise ValidationError(f"Unsupported format. Allowed: {', '.join(sorted(settings.ALLOWED_AUDIO_EXTENSIONS))}")


def validate_audio_size(value) -> None:
    max_bytes = settings.MAX_AUDIO_UPLOAD_MB * 1024 * 1024
    if value.size > max_bytes:
        raise ValidationError(f"File too large. Maximum size is {settings.MAX_AUDIO_UPLOAD_MB} MB.")
