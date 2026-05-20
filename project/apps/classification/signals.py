from django.db.utils import OperationalError, ProgrammingError
from django.dispatch import receiver
from django.db.models.signals import post_migrate

from apps.classification.repositories.genre_repository import GenreRepository


@receiver(post_migrate)
def sync_genres_from_preprocessing_config(sender, **kwargs):
    if getattr(sender, "label", None) != "classification":
        return
    try:
        GenreRepository.sync_from_preprocessing_config()
    except (OperationalError, ProgrammingError, FileNotFoundError, ValueError):
        return
