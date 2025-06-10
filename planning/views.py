from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from planning.services import JiraService


class PlanningView(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = JiraService()

    def get_sprints(self, request):
        return Response(self.service.get_sprints())

    def get_unassigned_current_issues(self, request):
        return Response(self.service.get_unassigned_current_issues())

    def get_users_issues(self, request):
        return Response(self.service.get_users_issues())
