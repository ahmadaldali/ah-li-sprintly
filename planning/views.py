from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from planning.services.factory import PlanningServiceFactory


class PlanningView(ViewSet):
    service = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.service = PlanningServiceFactory.get_planning_service(self.kwargs.get('service_name'))

    def get_sprints(self, request, *args, **kwargs):
        return Response(self.service.get_sprints())

    def get_unassigned_current_issues(self, request, *args, **kwargs):
        return Response(self.service.get_unassigned_current_issues())

    def get_issues_by_user(self, request, *args, **kwargs):
        return Response(self.service.get_issues_by_user())

    def get_assignable_users(self, request, *args, **kwargs):
        return Response(self.service.get_assignable_users())

    def get_issue(self, request, id, *args, **kwargs):
        return Response(self.service.get_issue(id))

