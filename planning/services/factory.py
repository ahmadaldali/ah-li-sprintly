from sprintly.error import APIError
from .jira import JiraService
from .base import IPlanningService
from ..enums import PlanningServiceType


class PlanningServiceFactory:
    @staticmethod
    def get_planning_service(service: str) -> IPlanningService:
        if service == PlanningServiceType.JIRA.value:
            return JiraService()
        # elif service == "trello":
        #     return TrelloService()

        raise APIError(f"Unknown planning service: {service}", 500)
