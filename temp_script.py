import random
from core.models import Info,Products,Review, Store
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


user = User.objects.all().first()
store = random.choice(Store.objects.all())

# for i in range(50):
#     products[0].reviews.create(user=user, title=f"Review N {uuid.uuid4}", content={uuid.uuid4}, score=randint(1,6))
for _ in range(50):Products.objects.create(name=f"Producto random", quantity=5,store=store)

