from rest_framework import serializers

from challenge.models_api.user_models import User
from challenge.models_api.account_model import Accounts
from challenge.models_api.teams_accounts_model import TeamsMembersAccount, TeamsAccounst

from django.contrib.auth.models import User


class AuthUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_permissions', 'groups']


class AuthUserSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthUserUpdatedSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_permissions', 'groups', 'password']


class AccountsSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(required=True)
    customer_name = serializers.CharField(required=True)
    account_manager_name = serializers.CharField(required=True)

    class Meta:
        model = Accounts
        fields = "__all__"


# class UserSerializaer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = "__all__"

class TeamsAccountSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(required=True)

    # account = serializers.
    class Meta:
        model = TeamsAccounst
        fields = "__all__"


class TeamMembersAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamsMembersAccount
        fields = "__all__"


class TeamsWithAccountSerializer(serializers.ModelSerializer):
    account = AccountsSerializer(many=False)

    class Meta:
        model = TeamsAccounst
        fields = '__all__'


class TeamsMembersSerializer(serializers.ModelSerializer):
    user = AuthUserListSerializer()

    class Meta:
        model = TeamsMembersAccount
        fields = '__all__'
