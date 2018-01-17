from django.conf.urls import url

from dashboard import views

urlpatterns = [
    url(r'^china/$', views.china, name='dashboard-china'),
]
