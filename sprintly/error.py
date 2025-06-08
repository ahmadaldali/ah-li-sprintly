from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


class APIError(Exception):
  def __init__(self, message, status_code=None):
    super().__init__(message)
    self.status_code = status_code


def custom_exception_handler(exc, context):
    if isinstance(exc, APIError):
        return Response(
            {"detail": str(exc)},
            status=exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    # fallback to default handler
    return exception_handler(exc, context)
