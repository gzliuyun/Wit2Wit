from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Wit2Wit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')), #富文本编辑器
    url(r'^user/', include('user.urls', namespace='user')), # 用户
    url(r'^cart/', include('cart.urls', namespace='cart')), # 购物车
    url(r'^order/', include('order.urls', namespace='order')), # 订单
    url(r'^', include('goods.urls', namespace='goods')), #商品，因作为首页，所以url地址未填内容
]
