from __future__ import unicode_literals

from django.db import models

from aqi.backends import current_hour


class Stock(models.Model):
    symbol = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    current = models.FloatField()
    volume = models.FloatField()
    high = models.FloatField()
    high52w = models.FloatField()
    percent = models.FloatField()

    update_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'stock'
        ordering = ['city_code']
