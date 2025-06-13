from django.urls import path
from .views import PlanningView

get_sprints = PlanningView.as_view({'get': 'get_sprints'})
get_unassigned_current_issues = PlanningView.as_view({'get': 'get_unassigned_current_issues'})
get_users_issues = PlanningView.as_view({'get': 'get_users_issues'})
get_assignable_users = PlanningView.as_view({'get': 'get_assignable_users'})

urlpatterns = [
    path('sprints/', get_sprints, name='sprints'),
    path('unassigned-current-issues/', get_unassigned_current_issues, name='unassigned-current-issues'),
    path('users-issues/', get_users_issues, name='users-issues'),
    path('assignable-users/', get_assignable_users, name='assignable-users'),
]

