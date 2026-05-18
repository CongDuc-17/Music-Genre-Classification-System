from django.apps import AppConfig


class ClassificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.classification"
    label = "classification"

    def ready(self):
        from apps.classification import signals  # noqa: F401
