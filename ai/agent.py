from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os
import logging

from openai import OpenAI

logger = logging.getLogger(__name__)

load_dotenv()


class IAgentService(ABC):
    @abstractmethod
    def suggest_assigner(self, issue, issues): pass


class OpenAIService(IAgentService):
    def __init__(self):
        self.open_ai = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

    def suggest_assigner(self, issue, issues):
        prompt = f"""
          You are an AI assistant helping with Jira ticket analysis.

          Input Structure:

          - The **issue** is a JSON object with the following fields:
            - `id`: the unique identifier of the issue
            - `title`: the summary/title of the issue
            - `description`: a detailed description of the issue
            - `epic`: the epic name or None if not applicable

          - The **history** is an array of user objects, where each user has:
            - `id`: the user's unique identifier
            - `name`: the full name of the user
            - `issues`: a list of past issues the user has worked on, each with the same structure as the issue above (`id`, `title`, `description`, `epic`)

          Based on this information, suggest the most suitable developer to assign to the issue.

          Issue to be assigned:
          {issue}

          History of issues were assigned by users:
          {issues}

          NOTE: Start with focusing on the related issues using the epic.

          NOTE: Return your response as valid JSON only. Do not include any extra text, markdown, or formatting — just the JSON object.
          Use this format:

          {{
            "assigner": "<name of the most suitable developer>",
            "assigner_id": "<id of the most suitable developer>",
            "issue": "<title of the issue to be assigned>",
            "reason": "<brief explanation of why this developer is a good fit>"
          }}
          """

        response = self.open_ai.chat.completions.create(
          model="gpt-4o-mini",
          # model="gpt-4.1",
          messages=[
            {"role": "user", "content": prompt}
          ],
          temperature=0.5,
        )

        return response.choices[0].message.content.strip()
