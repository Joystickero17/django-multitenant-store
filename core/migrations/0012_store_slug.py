# Generated by Django 4.1.1 on 2022-10-03 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_products_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
    ]