# Generated by Django 4.1.5 on 2023-01-23 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_channelgroup_remove_notification_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity_id',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]