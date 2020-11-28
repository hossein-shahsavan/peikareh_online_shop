from django_filters import rest_framework
from.models import Product


class ProductFilter(rest_framework.FilterSet):

    def get_discount(self, queryset, name, value):
        return queryset.filter(discount__isnull=False)

    discount = rest_framework.BooleanFilter(method='get_discount')

    class Meta:
        fields = ("category__name", "popular", "discount")
        model = Product



