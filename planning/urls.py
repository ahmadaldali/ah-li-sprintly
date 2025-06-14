from django.urls import path
from .views import PlanningView

get_sprints = PlanningView.as_view({'get': 'get_sprints'})
get_unassigned_current_issues = PlanningView.as_view({'get': 'get_unassigned_current_issues'})
get_issues_by_user = PlanningView.as_view({'get': 'get_issues_by_user'})
get_assignable_users = PlanningView.as_view({'get': 'get_assignable_users'})
get_issue = PlanningView.as_view({'get': 'get_issue'})

urlpatterns = [
    path('sprints', get_sprints, name='sprints'),
    path('unassigned-current-issues', get_unassigned_current_issues, name='unassigned-current-issues'),
    path('issues-by-users', get_issues_by_user, name='issues-by-users'),
    path('assignable-users', get_assignable_users, name='assignable-users'),
    path('issues/<int:id>', get_issue, name='issue'),
]

