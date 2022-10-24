# Generated by Django 4.1.2 on 2022-10-24 01:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_config_whatsapp_number_wish_unique product per user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
