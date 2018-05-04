# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import uuid

from django.http import JsonResponse, HttpResponse

from .models import ExciseA, ExciseB


def a(request):
    for i in xrange(50):
        ExciseA.objects.create(name='hello world')
    return JsonResponse({'msg': 'success'})


def b(request):
    for i in xrange(50):
        ExciseB.objects.create(id=uuid.uuid1(), name='hello world')
    return JsonResponse({'msg': 'success'})


def c(request):
    return HttpResponse('hello world')
