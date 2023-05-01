from django.contrib import admin
from django.contrib.auth.models import User

from django.db import models as m

class EnglishUser(m.Model):
    user = m.OneToOneField(User, on_delete=m.DO_NOTHING)
    level_english = m.CharField(max_length=25)
    link_resume = m.CharField(max_length=255, default='')