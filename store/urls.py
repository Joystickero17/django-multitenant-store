from django.urls import path
from store.views import CategoriesView, ProductDetailView, StoreLoginView, StoreView, WishListView


urlpatterns = [
    path("", StoreView.as_view(), name="main_store_list"),
    path("wishlist/", WishListView.as_view(), name="wishlist"),
    path("<str:slug_store>", StoreView.as_view(), name="store_list"),
    path("<str:slug_store>/product/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoriesView.as_view(), name="categories_list"),
    
    
]