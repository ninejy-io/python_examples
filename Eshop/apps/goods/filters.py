from django.db.models import Q
import django_filters
from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text='最高价格')
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category__id=value)|Q(category__parent_category__id=value)|Q(category__parent_category__parent_category__id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']