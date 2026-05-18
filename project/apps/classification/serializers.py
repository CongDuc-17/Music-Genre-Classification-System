from rest_framework import serializers

from apps.classification.models import AudioFile, ClassificationResult, Genre
from apps.classification.validators import validate_audio_extension, validate_audio_size


class AudioUploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[validate_audio_extension, validate_audio_size])


class PredictByAudioIdSerializer(serializers.Serializer):
    audio_id = serializers.IntegerField(min_value=1)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "slug", "name", "description")


class AudioFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AudioFile
        fields = (
            "id",
            "original_filename",
            "duration_seconds",
            "sample_rate",
            "size_bytes",
            "uploaded_at",
            "file_url",
        )
        read_only_fields = fields

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and hasattr(obj.file, "url"):
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ClassificationResultSerializer(serializers.ModelSerializer):
    predicted_genre = GenreSerializer(read_only=True)
    audio = AudioFileSerializer(read_only=True)

    class Meta:
        model = ClassificationResult
        fields = (
            "id",
            "audio",
            "predicted_genre",
            "confidence",
            "probabilities",
            "num_chunks",
            "created_at",
        )
        read_only_fields = fields
