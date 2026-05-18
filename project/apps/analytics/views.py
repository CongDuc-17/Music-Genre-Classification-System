from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analytics.services import get_dashboard_stats


class AnalyticsStatsView(APIView):
    def get(self, request):
        return Response(get_dashboard_stats(request.user))
