from django.conf import settings
from django.db import models


class Genre(models.Model):
    slug = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


def user_audio_upload_to(instance: "AudioFile", filename: str) -> str:
    return f"audio/{instance.user_id}/{filename}"


class AudioFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="audio_files")
    file = models.FileField(upload_to=user_audio_upload_to)
    original_filename = models.CharField(max_length=255)
    duration_seconds = models.FloatField(default=0)
    sample_rate = models.IntegerField(null=True, blank=True)
    size_bytes = models.BigIntegerField(default=0)
    extra_metadata = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self):
        return self.original_filename


class ClassificationResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="classification_results",
    )
    audio = models.ForeignKey(AudioFile, on_delete=models.CASCADE, related_name="results")
    predicted_genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name="predictions")
    confidence = models.FloatField()
    probabilities = models.JSONField(default=dict)
    num_chunks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.predicted_genre.slug} ({self.confidence:.2f})"
