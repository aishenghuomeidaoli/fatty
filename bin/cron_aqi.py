# _*_ coding: utf-8 _*_
import os
import logging
import requests
import sys
import django

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_DIR)

env = 'settings_pro' if sys.argv[-1] == 'settings_pro' else 'settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fatty.%s" % env)

django.setup()

logger = logging.getLogger('aqi')


def main():
    logger.info('-------------start crontab-------------')
    resp = requests.get('http://api.weblist.site/aqi/start/')
    logger.info('crontab result: %s' % resp.content)
    logger.info('-------------finish crontab-------------')
    return


if __name__ == '__main__':
    main()
