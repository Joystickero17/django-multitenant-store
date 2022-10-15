from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView,ListView
from core.models.store import Store
from core.models.product import Products
from django.contrib import messages



class StoreView(ListView):
    template_name = "store.html"
    model= Products
    paginate_by = 20
    queryset= Products.objects.all()

    def get_queryset(self):
        print("C")
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
        print("slug_store", slug_store)
        current_store = Store.objects.filter(slug__iexact=slug_store).first()
        if not current_store:
            return context
        context["current_store"] = current_store
        return context

# Create your views here.
