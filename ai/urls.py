from django.urls import path, include
from .views import AIPlanningView

suggest_assigner = AIPlanningView.as_view({'post': 'suggest_assigner'})
suggest_assigner_epic = AIPlanningView.as_view({'post': 'suggest_assigner_epic'})

planning_service_urlpatterns = [
  path('suggest-assigner/<int:issue_id>', suggest_assigner, name='suggest-assigner'),
  path('suggest-assigner-epic/<int:issue_id>', suggest_assigner_epic, name='suggest-assigner-epic'),
]

urlpatterns = [
  path('<str:service_name>/', include(planning_service_urlpatterns)),
]
