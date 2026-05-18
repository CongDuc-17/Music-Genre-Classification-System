from pathlib import Path

from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.inference.inference_service import predict_genre_from_path
from ai.exceptions import AudioDecodeError
from apps.analytics.services import log_activity
from apps.classification.models import AudioFile
from apps.classification.repositories.classification_repository import ClassificationRepository
from apps.classification.repositories.genre_repository import GenreRepository
from apps.classification.serializers import (
    AudioUploadSerializer,
    ClassificationResultSerializer,
    PredictByAudioIdSerializer,
)
from apps.classification.services import ClassificationService


class ClassifyUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        ser = AudioUploadSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        file_obj = ser.validated_data["file"]
        service = ClassificationService()
        try:
            payload = service.classify_upload(request.user, file_obj)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(payload, status=status.HTTP_201_CREATED)


class ClassifyPredictView(APIView):
    """Re-run inference on an existing AudioFile owned by the user (new ClassificationResult)."""

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        if "file" in request.FILES:
            ser = AudioUploadSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            service = ClassificationService()
            try:
                payload = service.classify_upload(request.user, ser.validated_data["file"])
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(payload, status=status.HTTP_201_CREATED)

        ser = PredictByAudioIdSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        audio = AudioFile.objects.filter(pk=ser.validated_data["audio_id"], user=request.user).first()
        if not audio or not audio.file:
            return Response({"detail": "Audio not found."}, status=status.HTTP_404_NOT_FOUND)

        path = Path(audio.file.path)
        if not path.is_file():
            return Response({"detail": "Audio file missing on server."}, status=status.HTTP_410_GONE)

        try:
            prediction = predict_genre_from_path(str(path))
        except AudioDecodeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if prediction is None:
            return Response(
                {"detail": "Inference failed for this audio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        repo = ClassificationRepository()
        genres = GenreRepository()
        genre = genres.ensure_from_prediction_label(prediction["genre"])
        result = repo.create_result(
            user=request.user,
            audio=audio,
            genre=genre,
            confidence=prediction["confidence"],
            probabilities=prediction["probabilities"],
            num_chunks=prediction["num_chunks"],
        )
        log_activity(
            request.user,
            "reclassify",
            {"result_id": result.id, "audio_id": audio.id},
        )
        top_k = [
            {"genre": x["genre"], "score": x["score"], "score_percent": round(x["score"] * 100, 1)}
            for x in prediction.get("top_k_predictions", [])
        ]
        return Response(
            {
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
            },
            status=status.HTTP_201_CREATED,
        )


class ClassificationHistoryView(generics.ListAPIView):
    serializer_class = ClassificationResultSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def get_queryset(self):
        search = self.request.query_params.get("search") or None
        genre = self.request.query_params.get("genre") or None
        return ClassificationRepository.list_for_user(self.request.user, search=search, genre_slug=genre)


class ClassificationHistoryDetailDeleteView(APIView):
    def delete(self, request, pk):
        deleted, _ = ClassificationRepository.delete_result(request.user, pk)
        if not deleted:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
