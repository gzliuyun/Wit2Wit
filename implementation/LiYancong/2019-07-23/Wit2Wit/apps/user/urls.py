from django.conf.urls import url
from user.views import RegisterView, SendMessageView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^send_message$', SendMessageView.as_view(), name='send_message'),  # 发送短信验证码
    url(r'^login$', LoginView.as_view(), name='login'),  # 登录
    url(r'^logout$', LogoutView.as_view(), name='logout'),  # 退出登录

    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),  # 用户订单页
    url(r'^address$', AddressView.as_view(), name='address'),  # 用户地址页
    url(r'^$', UserInfoView.as_view(), name='user'),  # 用户信息页
]
