from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile

from ai.inference.inference_service import predict_genre_from_path
from ai.exceptions import AudioDecodeError
from apps.analytics.services import log_activity
from apps.classification.repositories.classification_repository import ClassificationRepository
from apps.classification.repositories.genre_repository import GenreRepository


class ClassificationService:
    def __init__(self, repo: ClassificationRepository | None = None, genre_repo: GenreRepository | None = None):
        self._repo = repo or ClassificationRepository()
        self._genres = genre_repo or GenreRepository()

    def classify_upload(self, user: User, uploaded: UploadedFile) -> dict[str, Any]:
        from ai.preprocessing.preprocessing import get_audio_metadata

        meta_disk: dict[str, Any] = {}
        tmp_path: str | None = None
        try:
            suffix = Path(uploaded.name).suffix.lower() or ".wav"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                for chunk in uploaded.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            try:
                meta_disk = get_audio_metadata(tmp_path)
                prediction = predict_genre_from_path(tmp_path)
            except AudioDecodeError as e:
                raise ValueError(str(e)) from e
        finally:
            if tmp_path is not None and os.path.isfile(tmp_path):
                os.unlink(tmp_path)

        if prediction is None:
            raise ValueError(
                "Inference produced no result. Check that the TensorFlow model loads and the "
                "audio file is not corrupt."
            )

        uploaded.seek(0)
        audio = self._repo.create_audio_file(
            user=user,
            django_file=uploaded,
            original_filename=uploaded.name,
            duration_seconds=float(meta_disk.get("duration_seconds") or 0),
            sample_rate=meta_disk.get("sample_rate"),
            size_bytes=int(meta_disk.get("size_bytes") or uploaded.size or 0),
            extra_metadata={"inference_meta": meta_disk},
        )

        genre = self._genres.ensure_from_prediction_label(prediction["genre"])
        result = self._repo.create_result(
            user=user,
            audio=audio,
            genre=genre,
            confidence=prediction["confidence"],
            probabilities=prediction["probabilities"],
            num_chunks=prediction["num_chunks"],
        )

        log_activity(
            user,
            "classify",
            {"result_id": result.id, "genre": genre.slug, "confidence": prediction["confidence"]},
        )

        top_k = [
            {"genre": x["genre"], "score": x["score"], "score_percent": round(x["score"] * 100, 1)}
            for x in prediction["top_k_predictions"]
        ]
        return {
            "result_id": result.id,
            "genre": genre.slug,
            "genre_name": genre.name,
            "confidence": prediction["confidence"],
            "confidence_percent": round(prediction["confidence"] * 100, 1),
            "probabilities": prediction["probabilities"],
            "probabilities_percent": {k: round(v * 100, 2) for k, v in prediction["probabilities"].items()},
            "top_k_predictions": top_k,
            "num_chunks": prediction["num_chunks"],
            "audio_id": audio.id,
            "audio_url": audio.file.url,
            "original_filename": audio.original_filename,
        }
