import os
import requests
from openai import OpenAI
from ai.services.base import IAIModelService
from ai.services.prompt import PromptService
from sprintly.error import APIError
from ..models import ChatMessage


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
                response_format={"type": "json_object"}
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

    def predict_efficient_developer(self, issues, session_id):
        prompt = self.prompt_service.predict_efficient_developer_prompt(issues)

        #  @todo might delete the previous conversion  - start a new thread.

        ChatMessage.objects.create(session_id=session_id, role="user", content=prompt)
        ai_reply = self._get_ai_response([{"role": "user", "content": prompt}])
        ChatMessage.objects.create(session_id=session_id, role="assistant", content=ai_reply)

        return ai_reply

    def predict_efficient_developer_followup(self, session_id, message):
        ChatMessage.objects.create(session_id=session_id, role="user", content=message)
        chat_history = ChatMessage.objects.filter(session_id=session_id).order_by("timestamp")
        messages = [{"role": m.role, "content": m.content} for m in chat_history]

        # @todo make sure message.length > 3 , they initial predication was made

        ai_reply = self._get_ai_response(messages)
        ChatMessage.objects.create(session_id=session_id, role="assistant", content=ai_reply)

        return ai_reply
