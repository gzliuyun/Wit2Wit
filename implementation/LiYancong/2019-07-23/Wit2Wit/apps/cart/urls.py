from django.conf.urls import url
from cart.views import CartAddView, CartInfoView, CartUpdateView, CartDeleteView

urlpatterns = [
    url(r'^addcart$', CartAddView.as_view(), name='addcart'),  # 购物车记录添加
    url(r'^$', CartInfoView.as_view(), name='cartinfo'),  # 购物车页面显示
    url(r'^updatecart$', CartUpdateView.as_view(), name='updatecart'),  # 购物车记录更新
    url(r'^deletecart$', CartDeleteView.as_view(), name='deletecart'),  # 购物车记录删除
]
