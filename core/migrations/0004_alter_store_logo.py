# Generated by Django 4.1 on 2022-08-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_store_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]