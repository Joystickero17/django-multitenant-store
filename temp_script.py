import random
from core.models import Info,Products,Review, Store
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

create_random_reviews()