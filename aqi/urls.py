from django.conf.urls import url

from aqi.views import aqi, cities

urlpatterns = [
    url(r'^current/', aqi.current, name='aqi-current'),
    url(r'^cities/', cities.cities, name='aqi-cities'),
]
