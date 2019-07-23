from django.conf.urls import url
from order.views import OrderPageView, OrderSubmitView

urlpatterns = [
    url(r'^confirm_order$', OrderPageView.as_view(), name='confirm_order'), # 提交订单页面显示
    url(r'^submit_order$', OrderSubmitView.as_view(), name='submit_order'), # 创建一个订单
]