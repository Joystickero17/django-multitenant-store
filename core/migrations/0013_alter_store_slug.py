# Generated by Django 4.1.1 on 2022-10-03 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_store_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
