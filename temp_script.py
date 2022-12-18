import random
from core.models import Info,Products,Review, Store, Brand, Category
from django.contrib.auth import get_user_model
import uuid
from core.controllers.coinbase_controller import create_charge, get_charge

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

#create_charge()
get_charge('fb3e46d8-1b41-488d-90a6-85debe93c8fb')