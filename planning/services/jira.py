import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

from sprintly.error import APIError
from .base import IPlanningService

load_dotenv()


class JiraService(IPlanningService):
    def __init__(self):
        self.domain = os.getenv("JIRA_DOMAIN")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.board_id = 68  # @todo to set once you connect with jira (jira connect)
        self.project_key = "YOB"  # @todo to set once you connect with jira (jira connect)
        self.project_id = 10105  # @todo to set once you connect with jira (jira connect)
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.base_url = f"https://{self.domain}/rest/agile/1.0"
        self.rest_api_url = f"https://{self.domain}/rest/api/3"

    def _get(self, url, params=None):
        try:
            query_params = params.copy() if params else {}

            if not params or not params.get('maxResults'):
                query_params['maxResults'] = 1000

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

    @staticmethod
    def _format_issue(issue):
        fields = issue.get('fields', {})

        return {
          'id': issue.get('id'),
          'title': fields.get('summary'),
          #'description': fields.get('description'),
          'epic': fields.get('epic', {}).get('summary') if fields.get('epic') else None,
          'story_points': fields.get('customfield_10023') if fields.get('customfield_10023', 0) else 0,
          'sprints': len(fields.get('closedSprints', []))
        }

    def _get_issues_by_user_source(self, source_items, use_sprint=False):
        users_by_id = {}
        user_issue_ids = {}

        for user in self.get_assignable_users():
            user_id = user.get('accountId')
            display_name = user.get('displayName')

            if not user_id or not display_name:
                continue

            users_by_id[user_id] = {
              "id": user_id,
              "name": display_name,
              "issues": []
            }
            user_issue_ids[user_id] = set()

        for item in source_items:  # item is either a sprint or an epic issue
            issues = self.get_issues(item.get("id")) if use_sprint else [item]
            for issue in issues:
                fields = issue.get("fields", {})
                assignee = fields.get("assignee")

                if assignee:
                    user_id = assignee.get("accountId")
                    if user_id in users_by_id:
                        issue_id = issue.get("id")
                        if issue_id not in user_issue_ids[user_id]:
                            users_by_id[user_id]["issues"].append(self._format_issue(issue))
                            user_issue_ids[user_id].add(issue_id)

        return list(users_by_id.values())

    def get_sprints(self):
        url = f"{self.base_url}/board/{self.board_id}/sprint"
        sprints = self._get(url).get("values", [])

        sorted_sprints = sorted(
          sprints,
          key=lambda s: s.get('createdDate', ''),
          reverse=True
        )

        return sorted_sprints[:5]

    def get_current_sprint(self):
        url = f"{self.base_url}/board/{self.board_id}/sprint"
        return self._get(url, {"state": "active"}).get("values", [])

    def get_issues(self, sprint_id):
        if not sprint_id:
            return []
        url = f"{self.base_url}/sprint/{sprint_id}/issue"

        return self._get(url).get("issues", [])

    def get_issues_for_epic(self, epic_key):
        url = f"""{self.rest_api_url}/search?jql="epic link"={epic_key}"""

        return self._get(url).get("issues", [])

    def get_current_issues(self):
        return self.get_issues(self.get_current_sprint()[0].get("id"))

    def get_unassigned_current_issues(self):
        return [
            self._format_issue(issue) for issue in self.get_current_issues()
            if not issue.get("fields", {}).get("assignee")
        ]

    def get_issues_by_user(self):
        return self._get_issues_by_user_source(self.get_sprints(), use_sprint=True)

    def get_issues_by_user_for_epic(self, epic_key):
        return self._get_issues_by_user_source(self.get_issues_for_epic(epic_key), use_sprint=False)

    def get_assignable_users(self):
        url = f"{self.rest_api_url}/user/assignable/search?project={self.project_key}"

        return self._get(url, {"state": "active"})

    def get_issue(self, issue_id):
        url = f"{self.base_url}/issue/{issue_id}"
        issue = self._get(url)

        return issue

    def get_issue_types(self):
        url = f"{self.base_url}/issuetype/project?projectId={self.project_id}"

        return self._get(url)
