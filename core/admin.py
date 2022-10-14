from django.contrib import admin
from core.models import Products
from core.models.brand import Brand
from core.models.media import Media
from core.models.store import Store
# Register your models here.

admin.site.register(Products)
admin.site.register(Brand)
admin.site.register(Media)
admin.site.register(Store)
