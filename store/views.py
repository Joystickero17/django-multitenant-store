from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView,ListView, DetailView,DeleteView,View
from core.models.assistance import Assistance
from core.models.brand import Brand
from core.models.order import Order
from core.models.product_order import CartItem, ProductOrder
from core.models.category import Category
from core.models.store import Store
from core.models.product import Products
from django.contrib import messages
from django.shortcuts import get_object_or_404
from core.models.wishlist import Wish
from django_filters.views import FilterView
from django.db.models import Q,Count
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from store.filters import ProductFilter

class TermsView(TemplateView):
    template_name = "terms_conditions.html"

class AssistanceDetailView(LoginRequiredMixin,DetailView):
    template_name = "assistance_chat.html"
    model = Assistance
    queryset = Assistance.objects.all()

class AssistanceView(LoginRequiredMixin,ListView):
    template_name = "assistance_list.html"
    model = Assistance
    queryset = Assistance.objects.all()
    paginate_by = 20
    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)

class HelpChatView(LoginRequiredMixin,TemplateView):
    template_name = "client_chat.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        if not request.user.cart.cart_items.all().exists():
            messages.error("Debe agregar productos al carrito antes de solicitar la asistencia")
            return redirect(reverse("main_store_list"))
        return super().dispatch(request, *args, **kwargs)


class StoreListView(ListView):
    template_name = "shop_list.html"
    model = Store
    queryset = Store.objects.all()
    paginate_by = 20
    
class CategoriesView(ListView):
    template_name = "categories_list.html"
    model = Category
    queryset = Category.objects.all()
    paginate_by = 20

class RedirectOnGet(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse("main_store_list"))

class AddItemToWish(LoginRequiredMixin,RedirectOnGet,View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product")
        product = Products.objects.filter(id=product_id).first()
        if not product:
            messages.error(request, "Producto inválido")
            return redirect(request.META.get('HTTP_REFERER'))

        Wish.objects.create(
            product=product,
            user=request.user
        )
        messages.success(request, "Agregado a la lista de deseos Exitosamente")
        return redirect(request.META.get('HTTP_REFERER'))

class RemoveItemFromWish(LoginRequiredMixin,RedirectOnGet,View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product")
        product = Products.objects.filter(id=product_id).first()
        if not product:
            messages.error(request, "Producto inválido")
            return redirect(request.META.get('HTTP_REFERER'))

        request.user.wish_list.filter(product=product).delete()
        messages.success(request, "Removido de la lista de deseos Exitosamente")
        return redirect(request.META.get('HTTP_REFERER'))

class RemoveItemFromCart(LoginRequiredMixin,RedirectOnGet,View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product")
        product = Products.objects.filter(id=product_id).first()
        return_args = {
            "product_slug": product.product_slug,
            "slug_store":product.store.slug
        }

        if not product:
            messages.error(request, "Producto inválido")
            return redirect(request.META.get('HTTP_REFERER'))
        
        request.user.cart.cart_items.filter(product=product).delete()
        messages.success(request, "Producto Eliminado con éxito del Carrito")
        return redirect(request.META.get('HTTP_REFERER'))

class AddItemToCart(LoginRequiredMixin,RedirectOnGet,View):
    def post(self, request, *args, **kwargs):
        quantity = request.POST.get("quantity")
        product_id = request.POST.get("product")
        product = Products.objects.filter(id=product_id).first()
        return_args = {
            "product_slug": product.product_slug,
            "slug_store":product.store.slug
        }
        
        if not quantity:
            messages.error(request, "Cantidad inválida")
            return redirect(request.META.get('HTTP_REFERER'))

        if not product:
            messages.error(request, "Producto inválido")
            return redirect(request.META.get('HTTP_REFERER'))

        if not quantity.isdigit():
            messages.error(request, "Cantidad inválida")
            return redirect(request.META.get('HTTP_REFERER'))

        quantity = int(quantity)
        if quantity < 1 or quantity > product.quantity:
            messages.error(request, "Cantidad es mayor al stock existente")
            return redirect(request.META.get('HTTP_REFERER'))
        
        CartItem.objects.create(
            cart=request.user.cart,
            product=product,
            quantity=quantity,
            )
        messages.success(request, "Producto Agregado con éxito")
        return redirect(request.META.get('HTTP_REFERER'))

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
        if hasattr(self.request.user, "cart"):
            context["products_cart"] = list(self.request.user.cart.cart_items.all().values_list("product__id", flat=True))
        if hasattr(self.request.user, "wish_list"):
            context["wish_list"] = list(self.request.user.wish_list.all().values_list("product__id", flat=True))
            return context
        
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
        params = self.request.GET
        slug_page = self.kwargs.get("slug_store")
        free = params.get("free","").lower() == "true"
        print(self.request.GET.get("o") == "popular")
        # if self.request.GET.get("o") == "popular":
        #     queryset = queryset.annotate(review_count=Count("reviews")).order_by("-review_count")
        #     print(queryset.values())
        if slug_page:
            queryset = queryset.filter(store__slug__iexact=slug_page)

        if free:
            queryset = queryset.filter(
                Q(price__isnull=free) | Q(price=0)
                )
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
        context["most_sold"] = Products.objects.order_by("product_orders")[:5]
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
    
    def dispatch(self, request,*args, **kwargs):
        print("have items",request.user.cart.cart_items.exists())
        if not request.user.cart.cart_items.exists():

            messages.error(request, "Tu carrito no tiene productos, Agrega uno!")
            return redirect(reverse("main_store_list"))
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return self.request.user.cart.cart_items.all()

class StoreLoginView(auth_views.LoginView):
    next_page = "/store/"
    template_name = "login.html"
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            if request.user.store:
                return redirect(reverse("store_list"), slug_store=request.user.store.slug)
            return redirect(reverse("main_store_list"))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        user = form.get_user()
        if user.store:
            if self.request.GET.get("next"):
                return redirect(self.request.GET.get("next"))
            return redirect(reverse("store_list", kwargs={"slug_store":user.store.slug}))
        return redirect(reverse("main_store_list"))


class OrderView(LoginRequiredMixin, TemplateView):
    template_name = "user_orders.html"

class ProductOrderView(LoginRequiredMixin, DetailView):
    template_name = "order_detail.html"
    model = Order
    def dispatch(self, request, *args, **kwargs) :
        if not kwargs["pk"]:
            return redirect(reverse("main_store_list"))
        return super().dispatch(request, *args, **kwargs)


class StoreLogoutView(auth_views.LogoutView):
    next_page = "/store/"


class CoinbasePaymentView(TemplateView):
    template_name="coinbase_payment_success.html"


class CoinbasePaymentCanceledView(TemplateView):
    template_name="coinbase_payment_canceled.html"

class UserRegisterView(TemplateView):
    template_name = "register.html"
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main_store_list')
        return super().dispatch(request, *args, **kwargs)
