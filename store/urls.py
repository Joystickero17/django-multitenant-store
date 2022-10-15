from django.urls import path
from store.views import StoreView


urlpatterns = [
    path("", StoreView.as_view(), name="main_store_list"),
    path("<str:slug_store>", StoreView.as_view())
]