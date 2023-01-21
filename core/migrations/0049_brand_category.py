# Generated by Django 4.1.5 on 2023-01-14 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ForeignKey(help_text='Categoria relacionada a esta marca.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
    ]