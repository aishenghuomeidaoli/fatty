# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import json
from django.db.models import Q
from django.http import JsonResponse
import logging

from stock.models import Stock, StockKDay

logger = logging.getLogger('stock')


def detail(request, code):
    cond = Q(symbol=code) | Q(code=code)
    stock = Stock.objects.filter(cond)
    if stock.count() == 0:
        return JsonResponse({'code': '404', 'msg': u'未找到'})
    stock = stock.first()
    start = request.GET.get('start')
    if start:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
    else:
        today = datetime.date.today()
        start = today + datetime.timedelta(days=-30)
    rows = StockKDay.objects.filter(date__gte=start, stock=stock)\
        .order_by('date')
    data = [
        {
            'date': row.date,
            'open': row.open,
            'close': row.close,
            'low': row.low,
            'high': row.high,
            'price_change': row.price_change,
            'p_change': row.p_change,
            'volume': row.volume,
            'ma5': row.ma5,
            'ma10': row.ma10,
            'ma20': row.ma20
        } for row in rows
    ]
    return JsonResponse({'code': '200', 'msg': u'成功', 'data': data})
