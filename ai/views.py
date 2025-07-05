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

    def suggest_assigner_epic(self, request, issue_id, *args, **kwargs):
        return JsonResponse(self.service.suggest_assigner_by_epic(issue_id))

    def predict_efficient_developer(self, request, *args, **kwargs):
        return JsonResponse(self.service.predict_efficient_developer(session_id="12345"))

    def predict_efficient_developer_followup(self, request, *args, **kwargs):
        #  @todo: take the session id from the auth user. validate the request.
        user_input = request.POST.get("message")

        return JsonResponse(self.service.predict_efficient_developer_followup(session_id="12345", message=user_input))
