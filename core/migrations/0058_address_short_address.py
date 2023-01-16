# Generated by Django 4.1.5 on 2023-01-15 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_alter_order_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='short_address',
            field=models.CharField(help_text='Detalles de la direccion actual para fines de posicionamiento a la hora de envio', max_length=500, null=True),
        ),
    ]
