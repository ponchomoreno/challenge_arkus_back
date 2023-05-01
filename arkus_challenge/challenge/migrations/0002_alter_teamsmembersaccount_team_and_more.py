# Generated by Django 4.2 on 2023-04-27 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamsmembersaccount',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team_id', to='challenge.teamsaccounst'),
        ),
        migrations.AlterField(
            model_name='teamsmembersaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
