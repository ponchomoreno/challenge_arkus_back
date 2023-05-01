from django.shortcuts import render
from django.views.defaults import bad_request
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from challenge.serializers import AuthUserListSerializer, AccountsSerializer, TeamsAccountSerializer, \
    TeamsWithAccountSerializer, AuthUserUpdatedSerializer, AuthUserSaveSerializer, TeamsMembersSerializer, \
    TeamMembersAccountSerializer
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
# from challenge.models import Accounts, TeamsAccounst, TeamsMembersAccount
from .models_api.account_model import Accounts
from .models_api.teams_accounts_model import TeamsAccounst, TeamsMembersAccount
import jwt
from .validating_fields import validating_team_users
from django.db import transaction
from arkus_challenge import settings


def get_user_id_from_token(token):
    token = token.replace('Bearer', '').strip()
    decodeToken = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
    user = get_user_model().objects.get(pk=decodeToken['user_id'])
    return user


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_user(request):
    user = get_user_id_from_token(request.headers['Authorization'])
    if request.method == 'GET':
        if user.has_perm('auth.view_user'):
            usersdata = User.objects.all()
            if len(usersdata) == 0:
                return JsonResponse({'messageError': 'There is no content in users table'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                if user.is_staff or user.is_superuser:
                    user_serializer = AuthUserListSerializer(usersdata, many=True)
                    return JsonResponse({'data': user_serializer.data}, safe=False, status=status.HTTP_200_OK)
                else:
                    filterArrayUser = []
                    filterUser = {}
                    for user_reg in usersdata:
                        if user_reg.id == user.id:
                            filterUser = user_reg
                    user_serializer = AuthUserListSerializer(filterUser)
                    filterArrayUser.append(user_serializer.data)
                    return JsonResponse({'data': filterArrayUser}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to access to the users"})
    if request.method == 'POST':
        # GUARDAR EL NIVEL DE INGLES EN LA TABLA HEREDADA DE USER AUTH DE DJANGO
        if user.has_perm('auth.add_user'):
            user_data = JSONParser().parse(request)
            user_data['password'] = make_password(user_data['password'])
            user_serializer = AuthUserSaveSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse({'message': 'The user has been saved successfully'}, status=status.HTTP_200_OK)
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to create a user"})
    if request.method == 'DELETE':
        if user.has_perm('auth.delete_user'):
            idsusers = request.query_params.get('ids')
            arrayusers = idsusers.split(',')
            errosidsusers = []
            for userid in arrayusers:
                try:
                    user = User.objects.get(pk=int(userid))
                    user.delete()
                except User.DoesNotExist:
                    errosidsusers.append(userid)
            if len(errosidsusers) > 0:
                return JsonResponse({'messageError': 'There are some users that doesn´t exist in database'},
                                    status=status.HTTP_206_PARTIAL_CONTENT)
            return JsonResponse({'message': '{} User(s) was/were deleted successfully'.format(len(arrayusers))},
                                status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to delete users"})


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def api_user_by_id(request, id):
    user = get_user_id_from_token(request.headers['Authorization'])
    if user.has_perm('auth.view_user') and user.has_perm('auth.change_user'):
        try:
            userdata = User.objects.get(pk=id)
        except:
            return JsonResponse({'messageError': 'The user doesn´t exist in database'})
    else:
        raise PermissionDenied({"messageError": "You don't have permission to edit the user"})

    if request.method == 'GET':
        user_serializer = AuthUserUpdatedSerializer(userdata)
        return JsonResponse({'data': user_serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        userdatabody = JSONParser().parse(request)
        userdataserializer = AuthUserUpdatedSerializer(userdata, data=userdatabody)
        if userdataserializer.is_valid():
            userdataserializer.save()
            return JsonResponse({'message': 'The user was updated successfully'}, status=status.HTTP_200_OK)
        return JsonResponse({'messageError': userdataserializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_accounts(request):
    user = get_user_id_from_token(request.headers['Authorization'])
    if request.method == 'GET':
        if user.has_perm('challenge.view_accounts'):
            accounts_data = Accounts.objects.all().order_by('-updated_at')
            if len(accounts_data) == 0:
                return JsonResponse({'messageError': 'There is no content in accounts table'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                accounts_serializer = AccountsSerializer(accounts_data, many=True)
                return JsonResponse({'data': accounts_serializer.data}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"message": "You don't have permission to access to the accounts"})
    if request.method == 'POST':
        if user.has_perm('challenge.add_accounts'):
            account_data = JSONParser().parse(request)
            account_data_serializer = AccountsSerializer(data=account_data)
            if account_data_serializer.is_valid():
                account_data_serializer.save()
                return JsonResponse({'message': 'The account has been saved successfully'}, status=status.HTTP_200_OK)
            return JsonResponse(account_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"message": "You don't have permission to access"})
    if request.method == 'DELETE':
        if user.has_perm('challenge.delete_accounts'):
            idsaccounts = request.query_params.get('ids')
            arrayaccounts = idsaccounts.split(',')
            erroridsaccounts = []
            for accountid in arrayaccounts:
                try:
                    account = Accounts.objects.get(pk=int(accountid))
                    account.delete()
                except Accounts.DoesNotExist:
                    erroridsaccounts.append(accountid)
            if len(erroridsaccounts) > 0:
                return JsonResponse({'messageError': 'There are some accounts that it doesn´t exist in database'},
                                    status=status.HTTP_206_PARTIAL_CONTENT)
            return JsonResponse({'message': '{} Account(s) was/were deleted successfully'.format(len(arrayaccounts))},
                                status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to delete accounts"})


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def api_account_by_id(request, id):
    user = get_user_id_from_token(request.headers['Authorization'])
    if user.has_perm('challenge.view_accounts') and user.has_perm('challenge.change_accounts'):
        try:
            accountdata = Accounts.objects.get(pk=id)
        except:
            return JsonResponse({'messageError': 'The account doesn´t exist in database'})
    else:
        raise PermissionDenied({"message": "You don't have permission to edit the account"})

    if request.method == 'GET':
        account_serializer = AccountsSerializer(accountdata)
        return JsonResponse({'data': account_serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        accountdatabody = JSONParser().parse(request)
        accountdataserializer = AccountsSerializer(accountdata, data=accountdatabody)
        if accountdataserializer.is_valid():
            accountdataserializer.save()
            return JsonResponse({'message': 'The account was updated successfully'}, status=status.HTTP_200_OK)
        return JsonResponse(accountdataserializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_teams_accunts(request):
    user = get_user_id_from_token(request.headers['Authorization'])
    if request.method == 'GET':
        if user.has_perm('challenge.view_teamsaccounst'):
            teams_data = TeamsAccounst.objects.all()
            if len(teams_data) == 0:
                return JsonResponse({'messageError': 'There is no content in teams account table'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                teams_serializer = TeamsWithAccountSerializer(teams_data, many=True)
                return JsonResponse({'data': teams_serializer.data}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to access to the teams accounts"})
    if request.method == 'POST':
        if user.has_perm('challenge.add_teamsaccounst'):
            teams_data = JSONParser().parse(request)
            users_team = teams_data['users']
            if validating_team_users(teams_data) is False or len(teams_data['users']) == 0:
                return JsonResponse({'messageError': 'The users are required'})
            teams_data_serializer = TeamsAccountSerializer(data=teams_data)
            with transaction.atomic():
                if teams_data_serializer.is_valid():
                    teams_data_serializer.save()
                    for reg_user in users_team:
                        try:
                            # here i am validating that the user exists in database and that hasn´t been assigned
                            # to in a team
                            User.objects.get(pk=reg_user)
                            user_member_registered = TeamsMembersAccount.objects.filter(user=reg_user)
                            if len(user_member_registered) > 0:
                                transaction.set_rollback(True)
                                return JsonResponse({'messageError': 'The users can only be in a team'},
                                                    status=status.HTTP_400_BAD_REQUEST)
                            usermember = {'team': teams_data_serializer.data['id'], 'user': reg_user}
                            usermemberserializer = TeamMembersAccountSerializer(data=usermember)
                            if usermemberserializer.is_valid():
                                usermemberserializer.save()
                            else:
                                return JsonResponse(usermemberserializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        except User.DoesNotExist:
                            # Rollback in all involved tables if any user does not exist in database
                            transaction.set_rollback(True)
                            return JsonResponse({'mesaggeError': 'There is a user who is not active in database'})
                    return JsonResponse({'message': 'The team has been saved successfully'}, status=status.HTTP_200_OK)
                return JsonResponse(teams_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to create a team"})
    if request.method == 'DELETE':
        if user.has_perm('challenge.delete_teamsaccounst'):
            idsteams = request.query_params.get('ids')
            arrayteams = idsteams.split(',')
            erroridsteams = []
            for teamid in arrayteams:
                try:
                    team = TeamsAccounst.objects.get(pk=int(teamid))
                    team.delete()
                except TeamsAccounst.Does:
                    erroridsteams.append(teamid)
            if len(erroridsteams) > 0:
                return JsonResponse({'messageError': 'There are some teams that it doesn´t exist in database'},
                                    status=status.HTTP_206_PARTIAL_CONTENT)
            return JsonResponse({'message': '{} Team(s) was/were deleted successfully'.format(len(arrayteams))},
                                status=status.HTTP_200_OK)
        else:
            raise PermissionDenied({"messageError": "You don't have permission to delete teams"})


@api_view(['GET', 'PUT'])
def api_team_by_id(request, id):
    user = get_user_id_from_token(request.headers['Authorization'])
    if user.has_perm('challenge.view_teamsaccounst') and user.has_perm('challenge.change_teamsaccounst'):
        try:
            teamsdata = TeamsAccounst.objects.get(pk=id)
        except:
            return JsonResponse({'messageError': 'The team doesn´t exist in database'})
    else:
        raise PermissionDenied({"messageError": "You don't have permission to edit the team"})

    if request.method == 'GET':
        team_serializer = TeamsWithAccountSerializer(teamsdata)
        return JsonResponse({'data': team_serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        teamdatabody = JSONParser().parse(request)
        if validating_team_users(teamdatabody) is False or len(teamdatabody['users']) == 0:
            return JsonResponse({'messageError': 'The users are required'})
        users_team = teamdatabody['users']
        teamdataserializer = TeamsAccountSerializer(teamsdata, data=teamdatabody)
        with transaction.atomic():
            if teamdataserializer.is_valid():
                teamdataserializer.save()
                for reg_member in users_team:
                    try:
                        member = TeamsMembersAccount.objects.filter(user=int(reg_member))
                        member.delete()
                        usermember = {'team': id, 'user': reg_member}
                        usermemberserializer = TeamMembersAccountSerializer(data=usermember)
                        if usermemberserializer.is_valid():
                            usermemberserializer.save()
                        else:
                            return JsonResponse(usermemberserializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    except TeamsMembersAccount.DoesNotExist:
                        # Rollback in all involved tables if any user does not exist in database
                        transaction.set_rollback(True)
                        return JsonResponse({'messageError': 'There is a user who is not active in database'},
                                            status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse({'message': 'The team has been updated successfully'}, status=status.HTTP_200_OK)
            return JsonResponse(teams_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied({"messageError": "You don't have permission to update a team"})


@api_view(['GET'])
def api_users_by_team(request, id):
    user = get_user_id_from_token(request.headers['Authorization'])
    if user.has_perm('auth.view_user'):
        try:
            teamsmembersdata = TeamsMembersAccount.objects.filter(team=id)
        except:
            return JsonResponse({'messageError': 'The team doesn´t exist in database'})
    else:
        raise PermissionDenied({"messageError": "You don't have permission to edit the team"})

    if request.method == 'GET':
        if len(teamsmembersdata) == 0:
            return JsonResponse({'messageError': 'The team selected does not have members'},
                                status=status.HTTP_400_BAD_REQUEST)
        team_members_serializer = TeamsMembersSerializer(teamsmembersdata, many=True)
        return JsonResponse({'data': team_members_serializer.data}, status=status.HTTP_200_OK)
