from django.contrib import admin
from django.contrib.auth.models import User
from .account_model import Accounts
from django.db import models as m


class TeamsAccounst(m.Model):
    account = m.ForeignKey(Accounts, null=True, related_name='account_id', on_delete=m.DO_NOTHING)
    date_start = m.DateField(auto_now_add=True)
    date_end = m.DateField(auto_now_add=True)
    team_name = m.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Team {self.team_name}"


class TeamsMembersAccount(m.Model):
    team = m.ForeignKey(TeamsAccounst, related_name='team_id', on_delete=m.CASCADE)
    user = m.ForeignKey(User, related_name='user_id', on_delete=m.CASCADE)
