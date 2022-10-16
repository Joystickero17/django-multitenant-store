from random import randint
from core.models import Info,Products,Review
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


user = User.objects.all().first()
products = Products.objects.all().first()
# for i in range(50):
#     products[0].reviews.create(user=user, title=f"Review N {uuid.uuid4}", content={uuid.uuid4}, score=randint(1,6))
print(products.rating)

