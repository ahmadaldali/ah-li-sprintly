from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from ai.services.planning import AIPlanningService


class AIPlanningView(ViewSet):
    service = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.service = AIPlanningService(self.kwargs.get('service_name'))

    def suggest_assigner(self, request, issue_id, *args, **kwargs):
        return JsonResponse(self.service.suggest_assigner(issue_id))
