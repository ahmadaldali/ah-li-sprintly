from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from planning.services.factory import PlanningServiceFactory


class PlanningView(ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PlanningServiceFactory.get_planning_service("jira")

    def get_sprints(self, request):
        return Response(self.service.get_sprints())

    def get_unassigned_current_issues(self, request):
        return Response(self.service.get_unassigned_current_issues())

    def get_issues_by_user(self, request):
        return Response(self.service.get_issues_by_user())

    def get_assignable_users(self, request):
        return Response(self.service.get_assignable_users())

    def get_issue(self, request, id):
        return Response(self.service.get_issue(id))

