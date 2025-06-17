from django.urls import path, include
from .views import AIPlanningView

suggest_assigner = AIPlanningView.as_view({'post': 'suggest_assigner'})

planning_service_urlpatterns = [
  path('suggest-assigner/<int:issue_id>', suggest_assigner, name='suggest-assigner'),
]

urlpatterns = [
  path('<str:service_name>/', include(planning_service_urlpatterns)),
]
