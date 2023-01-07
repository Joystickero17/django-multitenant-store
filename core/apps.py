from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_basic_permission(sender, **kwargs):
    from core.choices.model_choices import RoleChoices
    from django.contrib.auth.models import Group, Permission
    for group in RoleChoices.CHOICES:
        group, _ = Group.objects.get_or_create(name=group[0])

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        post_migrate.connect(create_basic_permission, sender=self)
