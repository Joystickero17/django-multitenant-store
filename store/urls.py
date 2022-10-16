from django.urls import path
from store.views import ProductDetailView, StoreView


urlpatterns = [
    path("", StoreView.as_view(), name="main_store_list"),
    path("<str:slug_store>", StoreView.as_view()),
    path("<str:slug_store>/product/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail"),
    
]