# Generated by Django 4.1.5 on 2023-01-15 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_alter_products_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(help_text='Direccion de Envio de la orden', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.address'),
        ),
    ]