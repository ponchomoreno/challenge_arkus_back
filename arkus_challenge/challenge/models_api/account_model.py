from django.contrib import admin
from django.contrib.auth.models import User

from django.db import models as m


class Accounts(m.Model):
    account_name = m.CharField(max_length=255)
    customer_name = m.CharField(max_length=255)
    account_manager_name = m.CharField(max_length=255)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"Account {self.account_name}"