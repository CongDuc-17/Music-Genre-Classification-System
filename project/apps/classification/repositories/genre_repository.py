from __future__ import annotations

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
            defaults={"name": slug.replace("_", " ").title(), "description": ""},
        )
        return genre

    @staticmethod
    def all():
        return Genre.objects.all()
