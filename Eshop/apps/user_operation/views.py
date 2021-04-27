from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        用户收藏列表
    retrieve:
        判断某个商品是否已收藏
    create:
        收藏商品
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
    
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        return UserFavSerializer


class LeavingMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        获取留言列表
    create:
        添加留言
    delete:
        删除留言
    '''
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    '''
    list:
        获取用户地址列表
    create:
        添加用户地址
    update:
        更新用户地址
    delete:
        删除用户地址
    '''
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)