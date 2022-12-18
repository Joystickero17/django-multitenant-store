from django.urls import re_path, path, include
from core import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"cart", views.CartItemViewSet)
router.register(r"review", views.ReviewViewSet)
router.register(r"wishlist", views.WishListViewset)
router.register(r"store", views.StoreViewSet)
router.register(r"product", views.ProductViewSet)
router.register(r"user", views.UserConfigView)
router.register(r"category", views.CategoryViewset)
router.register(r"brand", views.BrandViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('most_sold/', views.MostSoldProductView.as_view()),
    path('max_price_product/', views.MaxPriceProduct.as_view()),
    path('user_info/', views.UserInfoView.as_view()),
    # path('login/', )
]