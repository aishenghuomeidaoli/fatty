from django.conf.urls import url

from stock import views

urlpatterns = [
    url(r'^detail/(?P<code>[0-9]{6})/$', views.detail, name='stock-detail'),
]
