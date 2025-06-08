from django.urls import path
from .views import PlanningView

get_sprints = PlanningView.as_view({'get': 'get_sprints'})
get_unassigned_current_issues = PlanningView.as_view({'get': 'get_unassigned_current_issues'})

urlpatterns = [
    path('sprints/', get_sprints, name='my-sprints'),
    path('unassigned-current-issues/', get_unassigned_current_issues, name='unassigned-current-issues'),
]
