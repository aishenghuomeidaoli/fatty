from django.conf.urls import url

from aqi.views import current

urlpatterns = [
    url(r'^current/', current, name='aqi-current'),
]
