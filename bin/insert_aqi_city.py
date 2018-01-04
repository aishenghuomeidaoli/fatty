# _*_ coding: utf-8 _*_
import os
import json
import sys
import django

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_DIR)

env = 'settings_pro' if sys.argv[-1] == 'settings_pro' else 'settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fatty.%s" % env)

django.setup()

from aqi.models import City


def main():
    city_file = os.path.join(PROJECT_DIR, 'bin/aqi_city.json')
    with open(city_file) as f:
        items = json.loads(f.read())
        for city_code, city_name in items.iteritems():
            if not City.objects.filter(city_code=city_code).exists():
                City.objects.create(city_code=city_code, city_name=city_name)


if __name__ == '__main__':
    main()
