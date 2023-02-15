import random
from core.models import Info,Products,Review, Store, Brand, Category,ProductOrder
from django.contrib.auth import get_user_model
import uuid
from core.controllers.coinbase_controller import create_charge, get_charge
from core.controllers import chart_controller
from core.models.order import Order, PaymentMethodChoices


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

def test_total_order():
    product1,product2,product3 = Products.objects.filter(price__isnull=False)[:3]
    random_user = random.choice(User.objects.all())
    data = {
        "paid":True,
        "user":random_user,
        "external_payment_id":"test_id",
        "payment_method":PaymentMethodChoices.COINBASE,
    }
    product_orders = [
        ProductOrder.objects.create(
            product=product1,
            quantity=random.randint(1,5),
            ),
        ProductOrder.objects.create(
            product=product2,
            quantity=random.randint(1,5),
            ),
        ProductOrder.objects.create(
            product=product3,
            quantity=random.randint(1,5),
            ),
    ]
    order = Order.objects.create(**data)
    order.product_orders.set(product_orders)
    print(order.total_order)

def delete_all_orders():
    Order.objects.all().delete()

# store : Store = Store.objects.get(id=2)
# print(chart_controller.current_store_controller(store,"month",year=2022,month=12))
# delete_all_orders()
#delete_all_orders()
#create_charge()
# get_charge('fb3e46d8-1b41-488d-90a6-85debe93c8fb')

# from core.controllers import paypal_controller

# # print(paypal_controller.generate_access_token())
# order = paypal_controller.create_order([{"amount":{
#     "currency_code":"USD",
#     "value":"100.0"
# }}])

# print(paypal_controller.capture_order(order.get("id")))
# from core.controllers.receipt_controller import generate_receipt


# order = Order.objects.all()[2]
# data = generate_receipt(order)
from core.controllers.export_controllers.chart import get_chart_csv_bytes, save_model
data = get_chart_csv_bytes({'chart': {1: 14.0, 2: 380.0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}, 'total_sales_count': 22, 'total_freelancers': 3, 'refunds': 0, 'visits': 1, 'products': 8, 'users': 2, 'reviews': 7})
save_model(data, "prueba.csv")



