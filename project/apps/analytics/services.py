from __future__ import annotations

from typing import Any

from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.analytics.models import UserActivity


def log_activity(user: User | None, action: str, metadata: dict[str, Any] | None = None) -> None:
    if user is None or not user.is_authenticated:
        return
    UserActivity.objects.create(user=user, action=action, metadata=metadata or {})


def get_dashboard_stats(for_user: User) -> dict[str, Any]:
    from apps.classification.models import ClassificationResult

    qs = ClassificationResult.objects.filter(user=for_user)
    total = qs.count()
    if total == 0:
        return {
            "total_classifications": 0,
            "most_common_genres": [],
            "genre_distribution": [],
            "uploads_by_day": [],
            "recent_activity_count_7d": 0,
        }

    genre_counts = (
        qs.values("predicted_genre__slug")
        .annotate(c=Count("id"))
        .order_by("-c")[:10]
    )
    distribution = list(
        qs.values("predicted_genre__name", "predicted_genre__slug").annotate(c=Count("id")).order_by("-c")
    )

    week_ago = timezone.now() - timezone.timedelta(days=7)
    recent = qs.filter(created_at__gte=week_ago).count()

    uploads_by_day = list(
        reversed(
            list(
                qs.annotate(day=TruncDate("created_at"))
                .values("day")
                .annotate(c=Count("id"))
                .order_by("-day")[:14]
            )
        )
    )

    return {
        "total_classifications": total,
        "most_common_genres": list(genre_counts),
        "genre_distribution": distribution,
        "uploads_by_day": uploads_by_day,
        "recent_activity_count_7d": recent,
    }


def get_global_stats() -> dict[str, Any]:
    """Admin / aggregate metrics (optional)."""
    from apps.classification.models import ClassificationResult

    total = ClassificationResult.objects.count()
    return {"total_classifications_all_users": total}
