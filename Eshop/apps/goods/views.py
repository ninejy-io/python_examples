from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer
from goods.filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    商品列表页, 分页, 过滤, 搜索, 排序
    '''
    queryset = Goods.objects.all()
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('=name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # modify click num
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品类别列表数据
    retrieve:
        商品分类详情
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    serializer_class = CategorySerializer


class BannerViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    serializer_class = BannerSerializer


class IndexCategoryViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True)
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    serializer_class = IndexCategorySerializer