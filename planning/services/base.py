from abc import ABC, abstractmethod


class IPlanningService(ABC):
    @abstractmethod
    def get_sprints(self): pass

    # issues not assigned from current sprint
    @abstractmethod
    def get_unassigned_current_issues(self): pass

    # get issues by active users
    @abstractmethod
    def get_issues_by_user(self): pass

    @abstractmethod
    def get_assignable_users(self): pass

    @abstractmethod
    def get_issue(self, issue_id): pass
