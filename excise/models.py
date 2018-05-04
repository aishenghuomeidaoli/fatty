from __future__ import unicode_literals

from django.db import models

from aqi.backends import current_hour


class ExciseA(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'excise_a'


class ExciseB(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'excise_b'
