from django.urls import path

from apps.classification.views import (
    ClassifyPredictView,
    ClassifyUploadView,
    ClassificationHistoryDetailDeleteView,
    ClassificationHistoryView,
)

urlpatterns = [
    path("upload/", ClassifyUploadView.as_view(), name="api-classify-upload"),
    path("predict/", ClassifyPredictView.as_view(), name="api-classify-predict"),
    path("history/", ClassificationHistoryView.as_view(), name="api-classify-history"),
    path("history/<int:pk>/", ClassificationHistoryDetailDeleteView.as_view(), name="api-classify-history-delete"),
]
