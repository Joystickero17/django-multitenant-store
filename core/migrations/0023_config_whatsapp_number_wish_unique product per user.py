# Generated by Django 4.1.2 on 2022-10-23 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_wish'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='whatsapp_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddConstraint(
            model_name='wish',
            constraint=models.UniqueConstraint(fields=('product', 'user'), name='unique product per user'),
        ),
    ]