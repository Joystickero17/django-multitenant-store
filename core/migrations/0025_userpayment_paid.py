# Generated by Django 4.1.6 on 2023-02-07 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_userpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpayment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]