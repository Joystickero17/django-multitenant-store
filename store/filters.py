from core.models.category import Category
from core.models.product import Products
from core.models.brand import Brand
from django.db.models import Count
import django_filters


class CustomOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.extra["choices"] +=[
            ("popular","-review_count")
        ]
    def filter(self, qs, value):
        if not isinstance(value,list):
            return super().filter(qs,value)
        if "popular" in value:
            return qs.annotate(review_count=Count("reviews")).order_by("-review_count")
        return super().filter(qs,value)

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    min_price = django_filters.NumberFilter(field_name="price",lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    free = django_filters.BooleanFilter(field_name="price", lookup_expr="isnull")
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all())

    o = CustomOrderingFilter(        # tuple-mapping retains order
        fields=(
            ('category', 'category'),
            ('name', 'product_name'),
            ('price', 'price'),
            ('created_at', '-created_at'),
            ("populart","-review_coun")
        ),
        )
    
    class Meta:
        model = Products
        fields = ["name", "price", "category", "brand"]
    
