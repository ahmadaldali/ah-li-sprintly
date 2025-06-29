from django.urls import path, include
from .views import AIPlanningView

suggest_assigner = AIPlanningView.as_view({'post': 'suggest_assigner'})
suggest_assigner_epic = AIPlanningView.as_view({'post': 'suggest_assigner_epic'})
predict_efficient_developer = AIPlanningView.as_view({'post': 'predict_efficient_developer'})
predict_efficient_developer_followup = AIPlanningView.as_view({'post': 'predict_efficient_developer_followup'})

planning_service_urlpatterns = {
  path('suggest-assigner/<int:issue_id>', suggest_assigner, name='suggest-assigner'),
  path('suggest-assigner-epic/<int:issue_id>', suggest_assigner_epic, name='suggest-assigner-epic'),
  path('predict-efficient-developer', predict_efficient_developer, name='predict-efficient-developer'),
  path('predict-efficient-developer-followup', predict_efficient_developer_followup,
       name='predict-efficient-developer-followup'),
}

urlpatterns = [
  path('<str:service_name>/', include(planning_service_urlpatterns)),
]
