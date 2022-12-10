from django.contrib import admin
from core.models import Products
from core.models.brand import Brand
from core.models.category import Category
from core.models.media import Media
from core.models.review import Review
from core.models.store import Store
from core.models import Config
from core.models.wishlist import Wish
from core.models.product_order import ProductOrder
from core.models.cart import Cart
# Register your models here.

admin.site.register(Products)
admin.site.register(Brand)
admin.site.register(Media)
admin.site.register(Store)
admin.site.register(Review)
admin.site.register(Config)
admin.site.register(Wish)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(ProductOrder)
