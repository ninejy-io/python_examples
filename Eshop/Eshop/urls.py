"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.views.generic import TemplateView
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from Eshop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from trade.views import ShoppingCartViewSet, OrderViewSet, AlipayView

router = DefaultRouter()

router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categorys', CategoryViewSet, base_name='categorys')

# 轮播图接口
router.register('banners', BannerViewSet, base_name='banners')

# 首页商品系列数据
router.register('indexgoods', IndexCategoryViewSet, base_name='indexgoods')

router.register('codes', SmsCodeViewSet, base_name='codes')
router.register('users', UserViewSet, base_name='users')

router.register('userfavs', UserFavViewSet, base_name='userfavs')
router.register('messages', LeavingMessageViewSet, base_name='messages')
router.register('address', AddressViewSet, base_name='address')

router.register('shopcarts', ShoppingCartViewSet, base_name='shopcart')
router.register('orders', OrderViewSet, base_name='orders')


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    path('', include(router.urls)),

    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

    path('docs/', include_docs_urls(title='Eshop')),

    # drf own auth
    path('api-token-auth/', views.obtain_auth_token),

    # The third part auth jwt
    re_path('^login/$', obtain_jwt_token),

    path('alipay/return/', AlipayView.as_view(), name='alipay'),

    path('', include('social_django.urls', namespace='social')),
]
