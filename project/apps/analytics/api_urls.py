from django.urls import path

from apps.analytics.views import AnalyticsStatsView

urlpatterns = [
    path("stats/", AnalyticsStatsView.as_view(), name="api-analytics-stats"),
]
