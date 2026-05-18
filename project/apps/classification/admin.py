from django.contrib import admin

from apps.classification.models import AudioFile, ClassificationResult, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "user", "duration_seconds", "uploaded_at")
    list_filter = ("uploaded_at",)


@admin.register(ClassificationResult)
class ClassificationResultAdmin(admin.ModelAdmin):
    list_display = ("predicted_genre", "user", "confidence", "created_at")
    list_filter = ("predicted_genre", "created_at")
