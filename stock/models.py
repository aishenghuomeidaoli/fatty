from __future__ import unicode_literals

from django.db import models

from aqi.backends import current_hour


class Stock(models.Model):
    symbol = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    current = models.FloatField()
    change = models.FloatField()
    volume = models.FloatField()
    percent = models.FloatField()
    high = models.FloatField()
    high52w = models.FloatField()
    low = models.FloatField()
    low52w = models.FloatField()

    pettm = models.FloatField()
    hasexist = models.BooleanField()
    amount = models.FloatField()
    type = models.IntegerField()
    marketcapital = models.FloatField()

    update_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '{0}({1})'.format(self.name, self.symbol)

    class Meta:
        db_table = 'stock'
        ordering = ['symbol']


class StockKDay(models.Model):
    stock = models.ForeignKey(Stock)
    code = models.CharField(max_length=32)
    date = models.DateField(auto_now=True, auto_now_add=True)

    open = models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    price_change = models.FloatField()
    p_change = models.FloatField()
    volume = models.FloatField()
    ma5 = models.FloatField()
    ma10 = models.FloatField()
    ma20 = models.FloatField()

    def __str__(self):
        return ''

    class Meta:
        db_table = 'stock_k_day'
        ordering = ['-date', 'code']
        unique_together = ('code', 'date')
