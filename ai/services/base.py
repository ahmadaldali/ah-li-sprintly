from abc import ABC, abstractmethod


class IAIPlanningService(ABC):
    @abstractmethod
    def suggest_assigner(self, issue_id): pass


class IAIModelService(ABC):
    @abstractmethod
    def suggest_developer(self, issue, issues): pass
