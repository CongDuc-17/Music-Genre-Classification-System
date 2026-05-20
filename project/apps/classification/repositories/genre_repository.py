from __future__ import annotations

from ai.utils.config import load_preprocessing_config
from apps.classification.models import Genre


class GenreRepository:
    @staticmethod
    def get_by_slug(slug: str) -> Genre | None:
        return Genre.objects.filter(slug=slug).first()

    @staticmethod
    def ensure_from_prediction_label(label: str) -> Genre:
        slug = label.lower().strip()
        genre, _ = Genre.objects.get_or_create(
            slug=slug,
            defaults={"name": GenreRepository.display_name(slug), "description": ""},
        )
        return genre

    @staticmethod
    def all():
        return Genre.objects.all()

    @staticmethod
    def display_name(slug: str) -> str:
        return slug.replace("_", " ").replace("-", " ").title().replace("Hiphop", "Hip-hop")

    @staticmethod
    def sync_from_preprocessing_config() -> None:
        cfg = load_preprocessing_config()
        for label in cfg["classes"]:
            slug = label.lower().strip()
            Genre.objects.update_or_create(
                slug=slug,
                defaults={"name": GenreRepository.display_name(slug), "description": ""},
            )
