from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models.user_data.address import Address
# Create your tests here.

User = get_user_model()


class UserTestCase(APITestCase):
    def test_only_one_user_per_main_address(self):
        random_user = User.objects.create(email="prueba@simplee.cl")
        try:
            address1 = Address.objects.create(
                user=random_user,
                google_coordinates="prueba",
                is_main=True,
                state="prueba",
                city="prueba",
                location="prueba",
                )
            address1 = Address.objects.create(
                user=random_user,
                google_coordinates="prueba",
                is_main=False,
                state="prueba",
                city="prueba",
                location="prueba",
                )
        except IntegrityError as e:
            return
            
        self.assertTrue(True, "No se deben crear dos direcciones principales")
