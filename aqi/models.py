from __future__ import unicode_literals

from django.db import models

from aqi.backends import current_hour


class City(models.Model):
    city_code = models.CharField(max_length=64, unique=True)
    city_name = models.CharField(max_length=256)
    lng = models.FloatField()
    lat = models.FloatField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.city_name

    class Meta:
        ordering = ['city_code']


class Aqi(models.Model):
    city = models.ForeignKey(City)
    aqi = models.IntegerField()
    pm2_5 = models.IntegerField()
    pm10 = models.IntegerField()
    so2 = models.IntegerField()
    no2 = models.IntegerField()
    co = models.FloatField()
    o3 = models.IntegerField()
    pollution_level = models.IntegerField()
    primary_contaminant = models.CharField(max_length=256)
    time = models.DateTimeField(default=current_hour())
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-time']
