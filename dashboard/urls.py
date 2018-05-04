from django.conf.urls import url

from dashboard import views

urlpatterns = [
    url(r'^aqi/$', views.aqi, name='dashboard-aqi'),
    url(r'^stock/$', views.stock, name='dashboard-stock'),
]
