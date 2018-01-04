# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.http import JsonResponse
import logging

from aqi.task import main
from aqi.backends import now

logger = logging.getLogger('aqi')


def start(request):
    task = main.delay()
    logger.info('add task: %s at %s' % (task, now()))
    return JsonResponse(
        {'code': '200', 'msg': u'成功', 'data': {'task_id': '%s' % task}})
