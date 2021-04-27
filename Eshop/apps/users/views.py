
import random
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from Eshop.settings import API_KEY
from users.models import VerifyCode
from users.serializers import SmsCodeSerializer, UserRegisterSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()


class CustomBackend(ModelBackend):
    '''
    用户自定义验证
    '''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsCodeSerializer

    def generate_code(self):
        '''
        生成4位数字的验证码
        '''
        _temp_list = []
        for _ in range(4):
            _temp_list.append(random.choice('1234567890'))
        return "".join(_temp_list)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(API_KEY)
        _code = self.generate_code()
        result = yun_pian.send_sms(_code, mobile)
        if result['code'] != 0:
            return Response({"mobile": result["msg"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            record_code = VerifyCode(code=_code, mobile=mobile)
            record_code.save()
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)

        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    用户
    '''
    # serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()