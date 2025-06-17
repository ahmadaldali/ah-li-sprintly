import os

from openai import OpenAI
from ai.services.base import IAIModelService
from ai.services.prompt import PromptService


class OpenAIService(IAIModelService):
    def __init__(self):
        self.open_ai = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

    def suggest_developer(self, issue, issues):
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
