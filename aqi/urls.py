from django.conf.urls import url

from aqi.views import start

urlpatterns = [
    url(r'^start/', start, name='aqi-start'),
]
