# Generated by Django 4.1.4 on 2022-12-25 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_alter_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(default='personally', help_text='Campo para saber como el cliente va a retirar la mercancia', max_length=100),
        ),
    ]
