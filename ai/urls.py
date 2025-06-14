from django.urls import path
from .views import AIView

suggest_assigner = AIView.as_view({'get': 'suggest_assigner'})

urlpatterns = [
    path('suggest-assigner/<int:issue_id>', suggest_assigner, name='suggest-assigner'),
]

