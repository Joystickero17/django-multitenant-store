from django.urls import path
from store.views import CategoriesView, ProductDetailView, StoreLoginView, StoreView, WishListView,CheckoutView


urlpatterns = [
    path("", StoreView.as_view(), name="main_store_list"),
    path("wishlist/", WishListView.as_view(), name="wishlist"),
    path("<str:slug_store>", StoreView.as_view(), name="store_list"),
    path("<str:slug_store>/product/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("categories/", CategoriesView.as_view(), name="categories_list"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    # path("remove_cart_item/<int:pk>/", DeleteitemFromCart.as_view(), name="checkout"),
]