from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView,ListView, DetailView
from core.models.store import Store
from core.models.product import Products
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView

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
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        get_object_or_404(Products, product_slug=self.kwargs.get("product_slug"), store__slug__iexact=self.kwargs.get("slug_store"))
        return queryset

class StoreView(FilterView):
    template_name = "store.html"
    model= Products
    paginate_by = 20
    queryset = Products.objects.all()
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        slug_page = self.kwargs.get("slug_store")
        if slug_page:
            return queryset.filter(store__slug__iexact=slug_page)
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
        if not current_store:
            return context
        context["current_store"] = current_store
        return context

# Create your views here.
