import os

import requests
from openai import OpenAI
from ai.services.base import IAIModelService
from ai.services.prompt import PromptService
from sprintly.error import APIError
import openai


class OpenAIService(IAIModelService):
    def __init__(self):
        self.open_ai = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

    def suggest_developer(self, issue, issues):
        try:
            prompt = PromptService().suggest_developer_prompt(issue, issues)

            response = self.open_ai.chat.completions.create(
                  model="gpt-4o-mini",
                  # model="gpt-4.1",
                  messages=[
                    {"role": "user", "content": prompt}
                  ],
                  temperature=0.5,
                )

            return response.choices[0].message.content.strip()

        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else 500
            raise APIError("Failed Openai API request: " + str(e), status_code)

        except requests.RequestException as e:
            raise APIError("Openai API connection error", 503)

        except Exception as e:
            raise APIError(f"openai exception: {type(e).__name__} - {e}", 500)


