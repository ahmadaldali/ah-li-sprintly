from abc import ABC, abstractmethod


class IAIPlanningService(ABC):
    @abstractmethod
    def suggest_assigner(self, issue_id): pass

    @abstractmethod
    def suggest_assigner_by_epic(self, issue_id): pass

    @abstractmethod
    def predict_efficient_developer(self, session_id): pass

    @abstractmethod
    def predict_efficient_developer_followup(self, session_id, message): pass


class IAIModelService(ABC):
    @abstractmethod
    def suggest_developer(self, issue, issues): pass

    @abstractmethod
    def predict_efficient_developer(self, issues, session_id): pass

    @abstractmethod
    def predict_efficient_developer_followup(self, session_id, message): pass
