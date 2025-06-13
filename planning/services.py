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
        self.board_id = 68  # @todo to set once you connect with jira (jira connect)
        self.project_key = "YOB"  # @todo to set once you connect with jira (jira connect)
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.base_url = f"https://{self.domain}/rest/agile/1.0"
        self.rest_api_url = f"https://{self.domain}/rest/api/3"

    def _get(self, url, params=None):
        try:
            query_params = params.copy() if params else {}

            response = requests.get(
              url,
              headers={"Accept": "application/json"},
              auth=self.auth,
              params=query_params
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
        sprints = self._get(url).get("values", [])

        sorted_sprints = sorted(
          sprints,
          key=lambda s: s.get('createdDate', ''),
          reverse=True
        )

        return sorted_sprints[:3]

    def get_current_sprint(self):
        url = f"{self.base_url}/board/{self.board_id}/sprint"
        return self._get(url, {"state": "active"}).get("values", [])

    def get_issues(self, sprint_id):
        if not sprint_id:
            return []
        url = f"{self.base_url}/sprint/{sprint_id}/issue"
        return self._get(url).get("issues", [])

    def get_current_issues(self):
        return self.get_issues(self.get_current_sprint()[0].get("id"))

    def get_unassigned_current_issues(self):
        return [
            issue for issue in self.get_current_issues()
            if not issue.get("fields", {}).get("assignee")
        ]

    def get_assignable_users(self):
        url = f"{self.rest_api_url}/user/assignable/search?project={self.project_key}"
        return self._get(url, {"state": "active"})

    def get_users_issues(self):
        assignees = {}
        user_issue_ids = {}

        for user in self.get_assignable_users():
            user_key = user['displayName']
            assignees[user_key] = []
            user_issue_ids[user_key] = set()

        for sprint in self.get_sprints():
            for issue in self.get_issues(sprint.get("id")):
                user = issue['fields']['assignee']
                if user:
                    user_key = user['displayName']
                    issue_info = {
                      'id': issue['id'],
                      'summary': issue['fields']['summary'],
                      'description': issue['fields']['description'],
                      'epic': issue['fields']['epic']['summary'] if issue['fields']['epic'] else None
                    }

                    if user_key in assignees:  # make sure this user is still active
                        if issue['id'] not in user_issue_ids[user_key]:
                            assignees[user_key].append(issue_info)
                            user_issue_ids[user_key].add(issue['id'])

        return assignees
