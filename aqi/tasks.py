# _*_ coding: utf-8 _*_
from __future__ import absolute_import, unicode_literals

import datetime
import logging
import requests
import urllib2

from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings

from aqi.models import City, Aqi
from aqi.backends import current_hour, now

logger = logging.getLogger('aqi')


def get_html(url):
    """获取指定url web内容

    :param url:
    :return:
    """
    try:
        html = requests.get(url).content
    except ValueError, urllib2.URLError:
        logger.info('!!! error !!! get html error')
        html = ''
    return html


def update_aqi():
    """解析所有城市AQI数据

    :return:
    """
    logger.info('------try to grab------')
    html = get_html(settings.AQI_URL)
    soup = BeautifulSoup(html, 'html5lib', from_encoding='gbk')
    citys = soup.select('tbody[id="legend_01_table"] tr')
    updated_at = soup.select_one('input[id="hour"]').get('value')
    try:
        year = int(updated_at[:4])
        month = int(updated_at[5:7])
        day = int(updated_at[8:10])
        hour = int(updated_at[11:13])
        time = datetime.datetime(year, month, day, hour)
    except Exception as e:
        logger.info(e.message)
        time = current_hour() + datetime.timedelta(hours=-1)
    if Aqi.objects.filter(time=time).exists():
        return
    for city in citys:
        pollution_level = city.get('class')[0] if city.get('class') else ''
        try:
            pollution_level = int(pollution_level.split('_')[-1])
            if pollution_level < 1 or pollution_level > 6:
                continue
        except Exception as e:
            logger.info(e.message)
            continue
        items = city.select('td')
        if not items or len(items) != 9:
            continue
        items = [item.getText() for item in items]
        city_name, aqi, pm2_5, pm10, so2, no2, co, o3, primary_contaminant = \
            items
        primary_contaminant = primary_contaminant.replace('\n', '')
        primary_contaminant = primary_contaminant.replace('\t', '')
        city_row = City.objects.filter(city_name=city_name).first()
        if not city_row:
            continue
        if Aqi.objects.filter(city=city_row, time=time).exists():
            continue
        Aqi.objects.create(
            city=city_row, aqi=int(aqi or 0),
            pm2_5=int(pm2_5 or 0),
            pm10=int(pm10 or 0),
            so2=int(so2 or 0),
            no2=int(no2 or 0),
            co=float(co or 0),
            o3=int(o3 or 0),
            pollution_level=pollution_level,
            primary_contaminant=primary_contaminant,
            time=time)
    return


def cycle():
    while True:
        try:
            update_aqi()
            logger.info(
                '==============finish grabing aqi at %s=============' % now())
            return
        except Exception, e:
            logger.info('!!!!!!failed cause: %s' % e)
            continue


@shared_task
def main():
    logger.info('==============start grabing aqi at %s=============' % now())
    cycle()


if __name__ == '__main__':
    main()
