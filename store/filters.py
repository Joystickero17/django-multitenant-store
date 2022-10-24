from core.models.product import Products
import django_filters



class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    min_price = django_filters.NumberFilter(field_name="price",lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    free = django_filters.BooleanFilter(field_name="price", lookup_expr="isnull")

    o = django_filters.OrderingFilter(        # tuple-mapping retains order
        fields=(
            ('category', 'category'),
            ('name', 'product_name'),
            ('price', 'price'),
        ),
        )
    class Meta:
        model = Products
        fields = ["name", "price"]