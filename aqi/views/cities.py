# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.http import JsonResponse
import logging

from aqi.models import City, SystemCache

logger = logging.getLogger('aqi')


def cities(request):
    if SystemCache.objects.filter(key='cities').exists():
        cache = SystemCache.objects.get(key='cities')
        data = json.loads(cache.cache)
    else:
        ds = []
        provinces = City.objects.filter(city_code__endswith='0000') \
            .order_by('city_code')
        for province in provinces:
            province_code = province.city_code
            city_ds = []
            rows = City.objects.filter(city_code__startswith=province_code[:2],
                                       city_code__endswith='00') \
                .exclude(city_code__endswith='0000').order_by('city_code')
            for city in rows:
                city_code = city.city_code

                country_ds = []
                countries = City.objects.filter(
                    city_code__startswith=city_code[:4]) \
                    .exclude(city_code__endswith='00').order_by('city_code')
                for country in countries:
                    country_ds.append(
                        {'name': country.city_name, 'code': country.city_code,
                         'lng': country.lng, 'lat': country.lat})
                city_ds.append(
                    {'name': city.city_name, 'code': city_code,
                     'lng': city.lng, 'lat': city.lat, 'children': country_ds}
                )
            ds.append(
                {'name': province.city_name, 'code': province_code,
                 'lng': province.lng, 'lat': province.lat, 'children': city_ds}
            )
        data = {'data': ds}
        cache = SystemCache(key='cities', cache=json.dumps(data))
        cache.save()
    data['code'] = '200'
    data['msg'] = u'成功'
    return JsonResponse(data)
