from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Wit2Wit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^learner/', include('learner.urls', namespace='learner')),
    url(r'^goods/', include('goods.urls', namespace='goods')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'order/', include('order.urls', namespace='order')),
]
