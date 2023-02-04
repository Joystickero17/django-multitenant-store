from django.urls import path
from store import views
from django.conf import settings


urlpatterns = [
    path("", views.StoreView.as_view(), name="main_store_list"),
    path("assistance/chat/<int:pk>/", views.AssistanceDetailView.as_view(), name="assistance_chat"),
    path("assistance/list/", views.AssistanceView.as_view(), name="assistance_list"),
    path("chat/help/", views.HelpChatView.as_view(), name="help_chat"),
    path("wishlist/", views.WishListView.as_view(), name="wishlist"),
    path("<str:slug_store>", views.StoreView.as_view(), name="store_list"),
    path("<str:slug_store>/product/<slug:product_slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("categories/", views.CategoriesView.as_view(), name="categories_list"),
    path("stores/", views.StoreListView.as_view(), name="stores_list"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("order_detail/", views.ProductOrderView.as_view(), name="order_detail"),
    path("order_detail/<str:pk>/", views.ProductOrderView.as_view(), name="order_detail"),
    path("order_list/", views.OrderView.as_view(), name="order_list"),
    # Coinbase vistas de Culminacion
    path("payment_success/", views.CoinbasePaymentView.as_view(), name=settings.COINBASE_SUCCESS_URL_NAME),
    path("payment_canceled/", views.CoinbasePaymentView.as_view(), name=settings.COINBASE_CANCELLED_URL_NAME),
    path("terms/conditions/", views.TermsView.as_view(), name="conditions"),
    path("user/register/", views.UserRegisterView.as_view(), name="user_register"),
    path("add_to_cart/", views.AddItemToCart.as_view(), name="add_to_cart"),
    path("remove_from_cart/", views.RemoveItemFromCart.as_view(), name="remove_from_cart"),
    path("add_to_wish/", views.AddItemToWish.as_view(), name="add_to_wish"),
    path("remove_from_wish/", views.RemoveItemFromWish.as_view(), name="remove_from_wish")
    # path("remove_cart_item/<int:pk>/", views.DeleteitemFromCart.as_view(), name="checkout"),
]