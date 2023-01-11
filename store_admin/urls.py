from django.urls import path,re_path
from django.views.generic import TemplateView
from store_admin import views


urlpatterns = [
    path('', views.VueAdminView.as_view(), name="admin_vue"),
    path('<path:otherpath>/', views.VueAdminView.as_view(), name="admin_vue")
]