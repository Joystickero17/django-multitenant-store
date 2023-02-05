from core.models.product import Products
from core.models.product_order import ProductOrder,Order
from core.models.store import Store
from core.utils.model_choices import OrderStatusChoices
from core.choices.model_choices import RoleChoices
from django.db.models import QuerySet,Sum,Count
from django.db.models.expressions import F
from django.utils.timezone import now
from calendar import monthrange
from django.contrib.auth import get_user_model

User = get_user_model()

def get_total_freelancers():
    return User.objects.filter(role=RoleChoices.FREELANCE).count()

def total_review_count(store:Store, **kwargs):
    queryset = Products.objects.all()
    
    if kwargs.get("current_store_stats"):
        queryset = queryset.filter(store=store)
    reviews = queryset.aggregate(review_count=Count("reviews")).get("review_count")
    return reviews

def total_sales_count(store: Store, **kwargs)->int:
    queryset = ProductOrder.objects.filter(
        order__payment_status=OrderStatusChoices.PAYMENT_SUCCESS, 
        order__isnull=False,
        )
    
    if kwargs.get("current_store_stats"):
        queryset = queryset.filter(product__store=store)
    
    return queryset.count()

def current_store_controller(store: Store, chart_type: str="year", **kwargs) ->QuerySet[ProductOrder]:
    product_orders = ProductOrder.objects.filter(
        order__payment_status=OrderStatusChoices.PAYMENT_SUCCESS, 
        order__isnull=False,
        )
    
    if kwargs.get("current_store_stats"):
        product_orders = product_orders.filter(product__store=store)
    
    year = kwargs.get("year") or now().date().year
    print(year, kwargs)
    if chart_type == "year":
        year_dict = dict.fromkeys(list(range(1,13)), 0)
        yearly_sales = product_orders.filter(
            order__created_at__date__year=year
        ).values("order__created_at__date__month").annotate(
            p_order_total=Sum(F("quantity")*F("product__price"))
            ).values_list(
                "order__created_at__date__month",
                "p_order_total"
                )
        year_dict.update(yearly_sales)
        return year_dict
    if chart_type == "month":
        month = kwargs.get("month") or 1 
        month_range = monthrange(year,month)[1]
        month_sales_dict = dict.fromkeys(list(range(1,month_range+1)),0)
        sales = product_orders.filter(
        order__created_at__date__year=year,
        order__created_at__date__month=month
        ).values("order__created_at__date__day").annotate(
        p_order_total=Sum(F("quantity")*F("product__price"))
        ).values_list(
            "order__created_at__date__day",
            "p_order_total"
            ) 
        month_sales_dict.update(sales)
        print(month_sales_dict)
        return month_sales_dict