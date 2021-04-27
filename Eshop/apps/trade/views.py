from datetime import datetime
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.permissions import IsOwnerOrReadOnly
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from utils.alipay import AliPay
from Eshop.settings import alipay_appid, app_private_key_path, alipay_public_key_path, \
                            app_notify_url, return_url, pay_debug_mode, alipay_gateway


class ShoppingCartViewSet(viewsets.ModelViewSet):
    '''
    购物车功能
    list:
        获取购物车内商品
    create:
        加入购物车
    update:
        更新购物车内商品
    delete:
        删除购物车内商品
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        _nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= _nums
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    订单管理
        list:
            获取用户订单列表
        create:
            新增订单
        delete:
            删除订单
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


class AlipayView(APIView):
    def get(self, request):
        '''
         处理支付包的 return_url 返回
         :param request:
         :return:
        '''
        processed_dict = {}
        for k, v in request.GET.items():
            processed_dict[k] = v
        
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid=alipay_appid,
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,
            app_notify_url=app_notify_url,
            return_url=return_url,
            debug=pay_debug_mode
        )

        verify_result = alipay.verify(processed_dict, sign)

        if verify_result is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            return redirect('index')
    
    def post(self, request):
        '''
        处理支付宝的 notify_url 返回
        :param request:
        :return:
        '''
        processed_dict = {}
        for k, v in request.POST.items():
            processed_dict[k] = v
        
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid=alipay_appid,
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,
            app_notify_url=app_notify_url,
            return_url=return_url,
            debug=pay_debug_mode
        )

        verify_result = alipay.verify(processed_dict, sign)

        if verify_result is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            
            return Response("success")
