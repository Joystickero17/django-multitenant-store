from django.urls import path
from django.views.generic import TemplateView
from store_admin import views


urlpatterns = [
    path("", views.VueAdminView.as_view(), name="admin_vue")
]