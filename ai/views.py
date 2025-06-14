from django.http import JsonResponse
from rest_framework.viewsets import ViewSet

from ai.services import AIService


class AIView(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AIService()

    def suggest_assigner(self, request, issue_id):
        data = self.service.suggest_assigner(issue_id)  # returns dict

        return JsonResponse(data)
