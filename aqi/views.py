# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http import JsonResponse
import logging

from aqi.models import Aqi

logger = logging.getLogger('aqi')


def current(request):
    rows = Aqi.objects.raw("""
        SELECT
          a.id                                     id,
          c.city_name                              city_name,
          c.city_code                              city_code,
          date_format(a.time, '%Y-%m-%d %H:%i:%S') time,
          a.aqi                                    aqi,
          a.pm2_5                                  pm2_5,
          a.pm10                                   pm10,
          a.so2                                    so2,
          a.no2                                    no2,
          a.co                                     co,
          a.o3                                     o3,
          a.pollution_level                        pl,
          a.primary_contaminant                    pc
        FROM aqi_aqi a, aqi_city c, (
                                      SELECT time
                                      FROM aqi_aqi
                                      ORDER BY time DESC
                                      LIMIT 1) r
        WHERE c.id = a.city_id AND r.time = a.time
        ORDER BY c.city_code;
    """)
    ds = []
    for row in rows:
        ds.append({
            'city_name': row.city_name,
            'city_code': row.city_code,
            'time': row.time,
            'aqi': row.aqi,
            'pm2_5': row.pm2_5,
            'pm10': row.pm10,
            'so2': row.so2,
            'no2': row.no2,
            'co': row.co,
            'o3': row.o3,
            'pollution_level': row.pl,
            'primary_contaminant': row.pc})
    time = ds[0].get('time', '') if ds else ''

    return JsonResponse(
        {'code': '200', 'msg': u'成功', 'data': {'time': time, 'data_set': ds}})
