from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.analytics.services import get_dashboard_stats, log_activity
from apps.classification.models import Genre
from apps.classification.repositories.classification_repository import ClassificationRepository
from apps.classification.serializers import AudioUploadSerializer
from apps.classification.services import ClassificationService
from apps.dashboard.forms import RegisterForm, SpotifyAuthForm, UserSettingsForm


class LoginView(DjangoLoginView):
    template_name = "authentication/login.html"
    authentication_form = SpotifyAuthForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        log_activity(form.get_user(), "login", {})
        return super().form_valid(form)


class RegisterView(FormView):
    template_name = "authentication/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("dashboard:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        log_activity(user, "register_web", {"username": user.username})
        messages.success(self.request, "Welcome - your account is ready.")
        return super().form_valid(form)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("dashboard:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            log_activity(request.user, "logout", {})
        return super().dispatch(request, *args, **kwargs)


class HomeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        stats = get_dashboard_stats(self.request.user)
        recent = ClassificationRepository.list_for_user(self.request.user)[:8]
        ctx["stats"] = stats
        ctx["recent_results"] = recent
        ctx["header_label"] = "Home"
        ctx["header_title"] = "Your studio"
        chart_rows = stats.get("genre_distribution") or []
        ctx["genre_chart_data"] = [
            {
                "name": row.get("predicted_genre__name") or row.get("predicted_genre__slug"),
                "count": row["c"],
            }
            for row in chart_rows
        ]
        return ctx


class UploadPageView(LoginRequiredMixin, TemplateView):
    template_name = "classification/upload.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["header_label"] = "Classify"
        ctx["header_title"] = "Upload track"
        return ctx


class UploadProcessView(LoginRequiredMixin, View):
    def post(self, request):
        upload = request.FILES.get("file")
        if not upload:
            messages.error(request, "Please choose an audio file.")
            return redirect("dashboard:upload")
        ser = AudioUploadSerializer(data={"file": upload})
        if not ser.is_valid():
            messages.error(request, "Invalid file - use mp3, wav, or ogg under the size limit.")
            return redirect("dashboard:upload")

        try:
            result = ClassificationService().classify_upload(request.user, ser.validated_data["file"])
        except ValueError as e:
            messages.error(request, str(e))
            return redirect("dashboard:upload")

        request.session["last_prediction"] = result
        messages.success(request, f"Classified as {result['genre_name']}")
        return redirect("dashboard:upload_result")


class UploadResultView(LoginRequiredMixin, TemplateView):
    template_name = "classification/result.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["prediction"] = self.request.session.get("last_prediction")
        ctx["header_label"] = "Result"
        ctx["header_title"] = "Prediction"
        return ctx


class HistoryView(LoginRequiredMixin, TemplateView):
    template_name = "classification/history.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search = self.request.GET.get("q")
        genre = self.request.GET.get("genre")
        ctx["results"] = ClassificationRepository.list_for_user(self.request.user, search=search, genre_slug=genre)
        ctx["search"] = search or ""
        ctx["genre_filter"] = genre or ""
        ctx["header_label"] = "Library"
        ctx["header_title"] = "History"
        ctx["all_genres"] = Genre.objects.all()
        return ctx


class HistoryDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        deleted, _ = ClassificationRepository.delete_result(request.user, pk)
        if deleted:
            messages.success(request, "Removed from history.")
        else:
            messages.error(request, "Item not found.")
        return redirect("dashboard:history")


class AnalyticsPageView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/analytics.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        stats = get_dashboard_stats(self.request.user)
        ctx["stats"] = stats
        ctx["header_label"] = "Insights"
        ctx["header_title"] = "Analytics"
        ctx["genre_chart_data"] = [
            {
                "name": row.get("predicted_genre__name") or row.get("predicted_genre__slug"),
                "count": row["c"],
            }
            for row in (stats.get("genre_distribution") or [])
        ]
        ctx["uploads_series"] = [
            {"day": row["day"].isoformat() if row.get("day") else "", "count": row["c"]}
            for row in (stats.get("uploads_by_day") or [])
        ]
        return ctx


class SettingsView(LoginRequiredMixin, FormView):
    template_name = "dashboard/settings.html"
    form_class = UserSettingsForm
    success_url = reverse_lazy("dashboard:settings")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["header_label"] = "Account"
        ctx["header_title"] = "Settings"
        return ctx

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["instance"] = self.request.user
        return kw

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Profile updated.")
        return super().form_valid(form)
