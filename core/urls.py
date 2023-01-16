from django.urls import re_path, path, include
from core import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"product_orders", views.ProductOrderView)
router.register(r"client_order", views.ClientOrderViewSet)
router.register(r"order", views.OrderViewSet)
router.register(r"cart", views.CartItemViewSet)
router.register(r"review", views.ReviewViewSet)
router.register(r"wishlist", views.WishListViewset)
router.register(r"store", views.StoreViewSet)
router.register(r"product", views.ProductViewSet)
router.register(r"user", views.UserConfigView)
router.register(r"category", views.CategoryViewset)
router.register(r"brand", views.BrandViewset)
router.register(r"regions", views.RegionModelViewSet)
router.register(r"subregions", views.CustomSubRegionView)
router.register(r"cities", views.CustomCityView)
router.register(r"same_user", views.SelfUserViewSet)
router.register(r"media", views.MediaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.TestWebSocketView.as_view()),
    path('most_sold/', views.MostSoldProductView.as_view()),
    path('max_price_product/', views.MaxPriceProduct.as_view()),
    path("register/", views.UserRegisterViewSet.as_view()),
    path('user_info/', views.UserInfoView.as_view()),
    path('payment/', views.PaymentView.as_view({"post":"post"})),
    path('paypal/orders/<str:paypal_order_id>/capture/', views.PaypalCaptureOrder.as_view()),
    path('chart/', views.HistoricSalesView.as_view()),
    # path('login/', )
]