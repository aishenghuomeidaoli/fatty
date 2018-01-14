# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http import JsonResponse
import logging

from aqi.models import Aqi

logger = logging.getLogger('aqi')


def current(request):
    last_time = Aqi.objects.first().time
    rows = Aqi.objects.raw("""
        SELECT
          a.id                  id,
          c.city_name           city_name,
          c.city_code           city_code,
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
        'city_name': row.city_name,
        'city_code': row.city_code,
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
