from django.urls import path

from apps.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.HomeDashboardView.as_view(), name="home"),
    path("upload/", views.UploadPageView.as_view(), name="upload"),
    path("upload/classify/", views.UploadProcessView.as_view(), name="upload_classify"),
    path("upload/result/", views.UploadResultView.as_view(), name="upload_result"),
    path("history/", views.HistoryView.as_view(), name="history"),
    path("history/<int:pk>/delete/", views.HistoryDeleteView.as_view(), name="history_delete"),
    path("analytics/", views.AnalyticsPageView.as_view(), name="analytics"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
