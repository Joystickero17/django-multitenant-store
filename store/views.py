from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView,ListView, DetailView,DeleteView
from core.models.brand import Brand
from core.models.product_order import CartItem, ProductOrder
from core.models.category import Category
from core.models.store import Store
from core.models.product import Products
from django.contrib import messages
from django.shortcuts import get_object_or_404
from core.models.wishlist import Wish
from django_filters.views import FilterView
from django.db.models import Q,Count
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

from store.filters import ProductFilter

class CategoriesView(TemplateView):
    template_name = "categories_list.html"

class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    slug_field = 'product_slug'
    slug_url_kwarg = 'product_slug'
    model = Products
    queryset = Products.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_store = self.kwargs.get("slug_store")
        current_store = Store.objects.filter(slug__iexact=slug_store).first()
        if not current_store:
            return context
        context["score_range"] = range(context["object"].rating)
        context["score_range_left"] = range(5-context["object"].rating)
        context["current_store"] = current_store
        context["related_products"] = Products.objects.filter(Q(store=current_store)|Q(category=context["object"].category)).exclude(id=context["object"].id)[0:10]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        get_object_or_404(Products, product_slug=self.kwargs.get("product_slug"), store__slug__iexact=self.kwargs.get("slug_store"))
        return queryset


class WishListView(LoginRequiredMixin, FilterView):
    template_name= "wishlist.html"
    model = Wish
    paginate_by= 20
    queryset= Wish.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class StoreView(FilterView):
    template_name = "store.html"
    model= Products
    paginate_by = 20
    queryset = Products.objects.all()
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset().annotate(review_count=Count("reviews"))
        slug_page = self.kwargs.get("slug_store")
        print(self.request.GET.get("o") == "popular")
        # if self.request.GET.get("o") == "popular":
        #     queryset = queryset.annotate(review_count=Count("reviews")).order_by("-review_count")
        #     print(queryset.values())
        if slug_page:
            queryset = queryset.filter(store__slug__iexact=slug_page)
        # if self.request.user.is_authenticated:
        #     return queryset
        return queryset

    def dispatch(self, request, *args, **kwargs):        
        slug_store = self.kwargs.get("slug_store")
        if not slug_store:
            return super().dispatch(request, *args, **kwargs)
        current_store = Store.objects.filter(slug__iexact=slug_store).first()
        if not current_store:
            messages.add_message(request, messages.WARNING,f"La tienda <strong>{slug_store}</strong> no fue encontrada, si crees que se trata de un error, por favor, comunicate con soporte",extra_tags='safe')
            return redirect(f'{reverse("main_store_list")}')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_store = self.kwargs.get("slug_store")
        current_store = Store.objects.filter(slug__iexact=slug_store).first()
        context["object_count"] = self.queryset.count()
        context["brand_list"] = Brand.objects.all()[:6]
        context["category_list"] = Category.objects.all()[:6]
        if hasattr(self.request.user, "cart"):
            context["products_cart"] = list(self.request.user.cart.cart_items.all().values_list("product__id", flat=True))
        context["category_param_list"] = [int(param) for param in dict(self.request.GET).get("category",[])]
        context["brand_param_list"] = [int(param) for param in dict(self.request.GET).get("brand",[])]
        if not current_store:
            return context
        context["current_store"] = current_store
        return context

# Create your views here.
# class DeleteitemFromCart(LoginRequiredMixin, DeleteView):
#     model = CartItem
#     success_url = "/store"
#     def dispatch(self, request, *args, **kwargs):
#         print(request)
#         return super().dispatch(request, *args, **kwargs)


class CheckoutView(LoginRequiredMixin, ListView):
    template_name = "checkout.html"
    model = CartItem
    
    def get_queryset(self):
        return self.request.user.cart.cart_items.all()

class StoreLoginView(auth_views.LoginView):
    next_page = "/store/"
    template_name = "login.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("main_store_list"))
        return super().dispatch(request, *args, **kwargs)


class StoreLogoutView(auth_views.LogoutView):
    next_page = "/store/"


class CoinbasePaymentView(TemplateView):
    template_name="coinbase_payment_success.html"


class CoinbasePaymentCanceledView(TemplateView):
    template_name="coinbase_payment_canceled.html"