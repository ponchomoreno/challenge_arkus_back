# from django.contrib import admin
# from django.contrib.auth.models import User
#
# from django.db import models as m
# # Register your models here.
#
# # class Users(m.Model):
# #     name = m.CharField(max_length=255)
# #     email = m.CharField(max_length=50)
# #     password = m.CharField(max_length=255)
# #     created_at = m.DateTimeField(auto_now_add=True)
# #     updated_at = m.DateTimeField(auto_now=True)
#
# class EnglishUser(m.Model):
#     user = m.OneToOneField(User, on_delete=m.DO_NOTHING)
#     level_english = m.CharField(max_length=25)
#     link_resume = m.CharField(max_length=255)
#
# class Accounts(m.Model):
#     account_name = m.CharField(max_length=255)
#     customer_name = m.CharField(max_length=255)
#     account_manager_name = m.CharField(max_length=255)
#     created_at = m.DateTimeField(auto_now_add=True)
#     updated_at = m.DateTimeField(auto_now=True)
#     def __str__(self) -> str:
#         return f"Account {self.account_name}"
#
# class TeamsAccounst(m.Model):
#     account = m.ForeignKey(Accounts, null=True, related_name='account', on_delete=m.DO_NOTHING)
#     date_start = m.DateField(auto_now_add=True)
#     date_end = m.DateField(auto_now_add=True)
#     team_name = m.CharField(max_length=255)
#
#     def __str__(self) -> str:
#         return f"Team {self.team_name}"
#
# class TeamsMembersAccount(m.Model):
#     team = m.ForeignKey(TeamsAccounst, related_name='teams', on_delete=m.DO_NOTHING)
#     user = m.ForeignKey(User, related_name='user', on_delete=m.DO_NOTHING)