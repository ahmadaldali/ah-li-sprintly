import json
from abc import ABC, abstractmethod

from ai.agent import OpenAIService
from planning.services import JiraService


class IAIService(ABC):
    @abstractmethod
    def suggest_assigner(self, issue_id): pass


class AIService(IAIService):
    def __init__(self, agent=None, planning_service=None):
        self.agent = agent or OpenAIService()
        self.planning_service = planning_service or JiraService()

    def suggest_assigner(self, issue_id):
        issue = self.planning_service.get_issue(issue_id)
        issues = self.planning_service.get_issues_by_user()

        return json.loads(self.agent.suggest_assigner(issue, issues))
