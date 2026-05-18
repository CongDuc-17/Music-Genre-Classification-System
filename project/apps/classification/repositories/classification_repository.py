from __future__ import annotations

from typing import Any

from django.contrib.auth.models import User
from django.db.models import QuerySet

from apps.classification.models import AudioFile, ClassificationResult, Genre


class ClassificationRepository:
    @staticmethod
    def create_audio_file(
        *,
        user: User,
        django_file,
        original_filename: str,
        duration_seconds: float,
        sample_rate: int | None,
        size_bytes: int,
        extra_metadata: dict[str, Any],
    ) -> AudioFile:
        return AudioFile.objects.create(
            user=user,
            file=django_file,
            original_filename=original_filename,
            duration_seconds=duration_seconds,
            sample_rate=sample_rate,
            size_bytes=size_bytes,
            extra_metadata=extra_metadata,
        )

    @staticmethod
    def create_result(
        *,
        user: User,
        audio: AudioFile,
        genre: Genre,
        confidence: float,
        probabilities: dict[str, float],
        num_chunks: int,
    ) -> ClassificationResult:
        return ClassificationResult.objects.create(
            user=user,
            audio=audio,
            predicted_genre=genre,
            confidence=confidence,
            probabilities=probabilities,
            num_chunks=num_chunks,
        )

    @staticmethod
    def list_for_user(user: User, search: str | None = None, genre_slug: str | None = None) -> QuerySet:
        qs = ClassificationResult.objects.filter(user=user).select_related("audio", "predicted_genre")
        if search:
            qs = qs.filter(audio__original_filename__icontains=search)
        if genre_slug:
            qs = qs.filter(predicted_genre__slug=genre_slug)
        return qs

    @staticmethod
    def delete_result(user: User, pk: int) -> tuple[int, dict[str, int]]:
        obj = ClassificationResult.objects.filter(pk=pk, user=user).select_related("audio").first()
        if not obj:
            return 0, {}
        audio = obj.audio
        deleted, detail = obj.delete()
        if not audio.results.exists():
            audio.file.delete(save=False)
            audio.delete()
        return deleted, detail
