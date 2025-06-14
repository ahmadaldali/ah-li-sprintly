from ai.enums import AIModelType
from ai.services.base import IAIModelService
from ai.services.openai import OpenAIService
from sprintly.error import APIError


class AIModelServiceFactory:
    @staticmethod
    def get_ai_agent(model: str) -> IAIModelService:
        if model == AIModelType.OPENAI.value:
            return OpenAIService()

        raise APIError(f"Unknown planning model: {model}", 500)
