import json

from ai.services.base import IAIPlanningService
from ai.services.factory import AIModelServiceFactory
from planning.services.factory import PlanningServiceFactory
from sprintly.error import APIError


class AIPlanningService(IAIPlanningService):
    def __init__(self, service_name):
        self.ai_model = AIModelServiceFactory.get_ai_agent("openai")
        self.planning_service = PlanningServiceFactory.get_planning_service(service_name)

    def suggest_assigner(self, issue_id):
        issue = self.planning_service.get_issue(issue_id)
        issues = self.planning_service.get_issues_by_user()

        return json.loads(self.ai_model.suggest_developer(issue, issues))

    def suggest_assigner_by_epic(self, issue_id):
        issue = self.planning_service.get_issue(issue_id)
        epic = issue.get('fields').get('epic')
        if epic:
            issues = self.planning_service.get_issues_for_epic(epic.get('key'))

            return json.loads(self.ai_model.suggest_developer(issue, issues))

        raise APIError("This service is not provided for this issue", 405)

    def predict_efficient_developer(self):
        issues = self.planning_service.get_issues_by_user()
        
        return json.loads(self.ai_model.predict_efficient_developer(issues))



