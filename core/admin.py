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
from core.models.user import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

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
admin.site.register(User, CustomUserAdmin)