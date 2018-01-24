# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.http import JsonResponse
import logging

from aqi.models import Aqi, SystemCache

logger = logging.getLogger('aqi')


def current(request):
    last_time = Aqi.objects.first().time
    SystemCache.objects.update_or_create()
    if SystemCache.objects.filter(key='aqi_current', time=last_time).exists():
        cache = SystemCache.objects.get(key='aqi_current', time=last_time)
        data = json.loads(cache.cache)
    else:
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
        data = {'data_set': ds}
        SystemCache.objects.update_or_create(
            key='aqi_current',
            defaults={'time': last_time, 'cache': json.dumps(data)})
    data['time'] = last_time.strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse({'code': '200', 'msg': u'成功', 'data': data})
