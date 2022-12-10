import random
from core.models import Info,Products,Review, Store, Brand, Category
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


store = random.choice(Store.objects.all())
#for _ in range(50):Products.objects.create(name=f"Producto random", quantity=5,store=store)

def create_random_reviews():
    user = User.objects.all().first()
    
    products = Products.objects.get(id=72)
    for _ in range(50):
        products.reviews.create(user=user, title=f"Review N {str(uuid.uuid4())[:4]}", content=f"{uuid.uuid4()}", score=random.randint(1,6))
def create_random_products():
    data = {
        "name": "producto Aleatorio",
        "category": random.choice(Category.objects.all()),
        "brand": random.choice(Brand.objects.all()),
        "quantity": random.randint(1,20),
        "store": random.choice(Store.objects.all())
    }

    for _ in range(50):
        Products.objects.create(**data)

query = User.objects.all()
user2 = query[1]
user2.info.document_number = "456897526"
user2.info.save()