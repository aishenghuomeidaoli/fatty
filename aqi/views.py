# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http import JsonResponse
import logging

from aqi.models import Aqi, City

logger = logging.getLogger('aqi')


def current(request):
    last_time = Aqi.objects.first().time
    rows = Aqi.objects.raw("""
        SELECT
          a.id                  id,
          c.city_name           city_name,
          c.city_code           city_code,
          c.lng                 lng,
          c.lat                 lat,
          a.aqi                 aqi,
          a.pm2_5               pm2_5,
          a.pm10                pm10,
          a.so2                 so2,
          a.no2                 no2,
          a.co                  co,
          a.o3                  o3,
          a.pollution_level     pl,
          a.primary_contaminant pc
        FROM aqi_aqi a, aqi_city c
        WHERE c.id = a.city_id AND a.time = '{0}'
        ORDER BY c.city_code;""".format(last_time))
    ds = [{
        'name': row.city_name,
        'code': row.city_code,
        'lng': row.lng,
        'lat': row.lat,
        'aqi': row.aqi,
        'pm2_5': row.pm2_5,
        'pm10': row.pm10,
        'so2': row.so2,
        'no2': row.no2,
        'co': row.co,
        'o3': row.o3,
        'pollution_level': row.pl,
        'primary_contaminant': row.pc
    } for row in rows]
    return JsonResponse({'code': '200', 'msg': u'成功',
                         'data': {'time': last_time, 'data_set': ds}})


def cities(request):
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
    return JsonResponse({'code': '200', 'msg': u'成功', 'data': ds})
