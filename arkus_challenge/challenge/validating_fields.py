from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse


def validating_team_users(users):
    users_flag = users.get('users', None)
    if users_flag is None:
        return False