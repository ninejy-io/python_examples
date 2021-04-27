import time
from rest_framework import serializers

from goods.models import Goods
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer

from Eshop.settings import alipay_appid, app_private_key_path, alipay_public_key_path, \
                            app_notify_url, return_url, pay_debug_mode, alipay_gateway
from utils.alipay import AliPay


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        'min_value': '商品数量不能小于一',
                                        'required': '请选择购买数量'
                                    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed
    
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=alipay_appid,
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,
            app_notify_url=app_notify_url,
            return_url=return_url,
            debug=pay_debug_mode
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = alipay_gateway + "?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid=alipay_appid,
            app_private_key_path=app_private_key_path,
            alipay_public_key_path=alipay_public_key_path,
            app_notify_url=app_notify_url,
            return_url=return_url,
            debug=pay_debug_mode
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = alipay_gateway + "?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        # 当前时间+user_id+随机数
        from random import randint
        order_sn = "{time_str}{userid}{randstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                userid=self.context["request"].user.id, randstr=randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs
    
    class Meta:
        model = OrderInfo
        fields = "__all__"