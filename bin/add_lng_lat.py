# _*_ coding: utf-8 _*_
import os
import requests
import sys
import django

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_DIR)

env = 'settings_pro' if sys.argv[-1] == 'settings_pro' else 'settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fatty.%s" % env)

django.setup()

from aqi.models import City


def main():
    url_base = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=baidu_ak&address='

    ds = []
    provinces = City.objects.filter(city_code__endswith='0000') \
        .order_by('city_code')
    for province in provinces:
        province_code = province.city_code
        city_ds = []
        cities = City.objects.filter(city_code__startswith=province_code[:2],
                                     city_code__endswith='00') \
            .exclude(city_code__endswith='0000').order_by('city_code')
        for city in cities:
            city_code = city.city_code

            country_ds = []
            countries = City.objects.filter(
                city_code__startswith=city_code[:4]) \
                .exclude(city_code__endswith='00').order_by('city_code')
            for country in countries:
                country_ds.append(
                    {'name': country.city_name, 'code': country.city_code,
                     'lng': country.lng, 'lat': country.lat})
            city_ds.append(
                {'name': city.city_name, 'code': city_code,
                 'lng': city.lng, 'lat': city.lat, 'children': country_ds}
            )
        ds.append(
            {'name': province.city_name, 'code': province_code,
             'lng': province.lng, 'lat': province.lat, 'children': city_ds}
        )
    for province_dic in ds:
        city_ds = province_dic.get('children', [])

        province_name = province_dic.get('name')
        province_code = province_dic.get('code')
        url = url_base + province_name.encode('utf-8')
        data = requests.get(url).json()
        if data.get('status') == 0:
            location = data.get('result', {}).get('location')
            lng = location.get('lng')
            lat = location.get('lat')
            City.objects.filter(city_code=province_code) \
                .update(lng=lng, lat=lat)
        else:
            print province_name, province_code
        for city_dic in city_ds:
            country_ds = city_dic.get('children', [])
            city_name = province_name + city_dic.get('name')
            city_code = city_dic.get('code')
            url = url_base + city_name.encode('utf-8')
            data = requests.get(url).json()
            if data.get('status') == 0:
                location = data.get('result', {}).get('location')
                lng = location.get('lng')
                lat = location.get('lat')
                City.objects.filter(city_code=city_code) \
                    .update(lng=lng, lat=lat)
            else:
                print city_name, city_code
            for country_dic in country_ds:
                name = city_name + country_dic.get('name')
                code = country_dic.get('code')
                url = url_base + name.encode('utf-8')
                data = requests.get(url).json()
                if data.get('status') == 0:
                    location = data.get('result', {}).get('location')
                    lng = location.get('lng')
                    lat = location.get('lat')
                    City.objects.filter(city_code=code) \
                        .update(lng=lng, lat=lat)
                else:
                    print name, code


if __name__ == '__main__':
    main()
