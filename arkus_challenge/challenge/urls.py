from django.urls import path
from challenge import views

urlpatterns = [
    path('challenge/users', views.api_user),
    path('challenge/accounts', views.api_accounts),
    path('challenge/users/<int:id>', views.api_user_by_id),
    path('challenge/accounts/<int:id>', views.api_account_by_id),
    path('challenge/teams', views.api_teams_accunts),
    path('challenge/teams/<int:id>', views.api_team_by_id),
    path('challenge/teams/members/<int:id>', views.api_users_by_team)
]
