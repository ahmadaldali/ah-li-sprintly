from abc import ABC, abstractmethod
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import logging

from sprintly.error import APIError

logger = logging.getLogger(__name__)

load_dotenv()


class IPlanningService(ABC):
    @abstractmethod
    def get_sprints(self): pass

    @abstractmethod
    def get_issues(self, sprint_id): pass

    @abstractmethod
    def get_current_issues(self): pass

    @abstractmethod
    def get_unassigned_current_issues(self): pass


class JiraService(IPlanningService):
    def __init__(self):
        self.domain = os.getenv("JIRA_DOMAIN")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.board_id = 1  # @todo to set once you connect with jira (jira connect)
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.base_url = f"https://{self.domain}/rest/agile/1.0"

    def _get(self, url, params=None):
        try:
            response = requests.get(
                url,
                headers={"Accept": "application/json"},
                auth=self.auth,
                params=params
            )
            response.raise_for_status()

            return response.json()
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else 500
            raise APIError("Failed Jira API request: " + str(e), status_code)
        except requests.RequestException as e:
            raise APIError("Jira API connection error", 503)

    def get_sprints(self):
        url = f"{self.base_url}/board/{self.board_id}/sprint"
        return self._get(url).get("values", [])

    def get_issues(self, sprint_id):
        if not sprint_id:
            return []
        url = f"{self.base_url}/sprint/{sprint_id}/issue"
        return self._get(url).get("issues", [])

    def get_current_issues(self):
        for sprint in self.get_sprints():
            if sprint.get("state") == "active":
                return self.get_issues(sprint.get("id"))
        return []

    def get_unassigned_current_issues(self):
        return [
            issue for issue in self.get_current_issues()
            if not issue.get("fields", {}).get("assignee")
        ]
