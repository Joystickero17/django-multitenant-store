from django.urls import re_path, path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"review", views.ReviewViewSet)
router.register(r"store", views.StoreViewSet)
router.register(r"product", views.ProductViewSet)
router.register(r"user", views.UserConfigView)
router.register(r"category", views.CategoryViewset)
router.register(r"brand", views.BrandViewset)


urlpatterns = [
    path('', include(router.urls))
]