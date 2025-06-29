import os
import requests
from openai import OpenAI
from ai.services.base import IAIModelService
from ai.services.prompt import PromptService
from sprintly.error import APIError


class OpenAIService(IAIModelService):
    def __init__(self):
        self.open_ai = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
        self.prompt_service = PromptService()
        # self.model = "gpt-4o-mini"
        self.model = "gpt-4.1"

    def _get_ai_response(self, messages):
        try:
            response = self.open_ai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else 500
            raise APIError(f"Failed OpenAI API request: {e}", status_code)
        except requests.RequestException:
            raise APIError("OpenAI API connection error", 503)
        except Exception as e:
            raise APIError(f"OpenAI exception: {type(e).__name__} - {e}", 500)

    def suggest_developer(self, issue, issues):
        prompt = self.prompt_service.suggest_developer_prompt(issue, issues)

        return self._get_ai_response([{"role": "user", "content": prompt}])

    def predict_efficient_developer(self, issues):
        prompt = self.prompt_service.predict_efficient_developer_prompt(issues)

        return self._get_ai_response([{"role": "user", "content": prompt}])
