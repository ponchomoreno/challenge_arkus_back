from django.contrib import admin
# from .models import Accounts, TeamsAccounst, TeamsMembersAccount, EnglishUser
from .models_api.user_models import EnglishUser
from .models_api.account_model import Accounts
from .models_api.teams_accounts_model import TeamsMembersAccount, TeamsAccounst

# Register your models here.
admin.site.register(Accounts)
admin.site.register(EnglishUser)
admin.site.register(TeamsAccounst)
admin.site.register(TeamsMembersAccount)
