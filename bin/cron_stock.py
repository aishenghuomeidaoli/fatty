# _*_ coding: utf-8 _*_
import os
import logging
import sys
import django

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_DIR)

env = 'settings_pro' if sys.argv[-1] == 'settings_pro' else 'settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fatty.%s" % env)

django.setup()

from stock.task import update_stocks

logger = logging.getLogger('stock')


def main():
    logger.info('-------------start crontab-------------')
    update_stocks.delay()
    logger.info('-------------finish crontab-------------')
    return


if __name__ == '__main__':
    main()
