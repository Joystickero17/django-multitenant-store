from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.timezone import now
from core.choices.model_choices import RoleChoices
from core.models.store import Store


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo que se usa para representar un Usuario en el sistema
    """
    email = models.EmailField(max_length=255, unique=True, help_text="Correo electronico del usuario")
    profile_img = models.ImageField(upload_to="media/", null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, help_text="Nombres del Usuario")
    last_name = models.CharField(max_length=255, blank=True, null=True, help_text="Apellidos del Usuario")
    about = models.TextField(blank=True, null=True, help_text="Breve descripcion acerca del usuario")
    is_active = models.BooleanField(default=True, help_text="Booleano para saber si la cuenta esta activada y operativa")
    is_staff = models.BooleanField(default=False, help_text="Booleano para saber si pertenece a los administradores")
    role = models.CharField(max_length=255, default=RoleChoices.BASE_USER, choices=RoleChoices.CHOICES, help_text="Literal para identificar uso de roles")
    date_joined = models.DateTimeField(default=now, help_text="fecha de ingreso al sistema")
    born_date = models.DateField(null=True, help_text="Fecha de nacimiento del usuario")
    store = models.ForeignKey(to=Store, on_delete=models.SET_NULL, null=True, help_text="tienda a la que pertenece, puede ser nulo en caso de ser cliente o freelance")
    phone_number = models.CharField(max_length=255, help_text="Numero de telefono del usuario")
    credits = models.FloatField(default=0, help_text="Creditos para retirar premios usuario")
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}" 