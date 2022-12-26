import django_filters
from .models import Variant
class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='contains')
    price = django_filters.RangeFilter()
    class Meta:
        model = Variant
        fields = ['price', 'title', "color"]