# Generated by Django 4.1.5 on 2023-01-15 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='aditional_info',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(help_text='Direccion de Envío de la orden', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.address'),
        ),
    ]