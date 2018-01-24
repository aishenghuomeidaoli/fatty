# _*_ coding: utf-8 _*_
from __future__ import absolute_import, unicode_literals

import datetime
import time
import logging

from celery import shared_task
from requests import Request, Session

from stock.models import Stock

logger = logging.getLogger('stock')

url_detail = 'https://xueqiu.com/S/{}'
url_stat = 'https://xueqiu.com/v4/stock/quote.json?code={0}&_={1}'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.81 Safari/537.36',
    'host': 'xueqiu.com',
}

s = Session()
s.get('https://xueqiu.com/', headers=headers)


def http(request):
    prepared = s.prepare_request(request)
    resp = s.send(prepared)
    return resp.json()


@shared_task
def update_stocks():
    url_all = 'https://xueqiu.com/stock/cata/stocklist.json?' \
              'page={page}&size=90&order=desc&orderby=code&type=11%2C12' \
              '&_={now}'
    for page in range(1, 65):
        url = url_all.format(**{'page': page, 'now': int(time.time() * 1000)})
        r = Request('GET', url, headers=headers)
        data = http(r)
        stocks = data['stocks']
        for stock in stocks:
            code = stock.get('code')
            name = stock.get('name')
            symbol = stock.get('symbol')
            if not symbol or not name or not code:
                continue
            current = stock.get('current')
            change = stock.get('change')
            volume = stock.get('volume')
            percent = stock.get('percent')
            high = stock.get('high')
            high52w = stock.get('high52w')
            low = stock.get('low')
            low52w = stock.get('low52w')
            pettm = stock.get('pettm')
            hasexist = stock.get('hasexist')
            amount = stock.get('amount')
            type = stock.get('type')
            marketcapital = stock.get('marketcapital')

            Stock.objects.update_or_create(symbol=symbol, defaults={
                'code': code,
                'name': name,
                'current': None if current == '' else current,
                'change': None if change == '' else change,
                'volume': None if volume == '' else volume,
                'percent': None if percent == '' else percent,
                'high': None if high == '' else high,
                'high52w': None if high52w == '' else high52w,
                'low': None if low == '' else low,
                'low52w': None if low52w == '' else low52w,
                'pettm': None if pettm == '' else pettm,
                'hasexist': None if hasexist == '' else hasexist,
                'amount': None if amount == '' else amount,
                'type': None if type == '' else type,
                'marketcapital':
                    None if marketcapital == '' else marketcapital,
            })
    return


def judge(code):
    """判断是否为上吊线

    :param code:
    :return:
    """
    url = url_stat.format(code, int(time.time() * 1000))
    r = Request('GET', url, headers=headers)
    data = http(r).values()[0]
    start, end, high, low = float(data['open']), float(data['current']), float(
        data['high']), float(data['low'])
    range_rise = abs(start - end)
    range_wave = abs(high - low)
    if range_rise != 0 and 3 * range_rise < range_wave:
        return int(range_wave / range_rise)
    return False


def stock_filter():
    """遍历查找

    :return:
    """
    data = {}
    count = 1
    for stock in constant.stock:
        count += 1
        if count > 500:
            break
        price = float(stock['current'])
        if price == 0 or 1 < price < 10:
            continue
        result = judge(stock['code'])
        if result:
            if result not in data:
                data[result] = [{'name': stock['name'],
                                 'url': url_detail.format(stock['code'])}]
            else:
                data[result].append({'name': stock['name'],
                                     'url': url_detail.format(stock['code'])})
    return data


@shared_task
def main():
    data = stock_filter()
    for i in sorted(data, reverse=True):
        print i, data[i]
        # session.commit()


def update_script():
    count = 1
    for stock in constant.stock:
        count += 1
        # if count > 100:
        #     break
        price = float(stock['current'])
        if price == 0 or 10 < price < 500:
            continue
        result = judge(stock['code'])
        if result:
            row = session.query(Stock).filter_by(code=stock['code'],
                                                 date=datetime.datetime.now().date()).first()
            if row:
                row.rate = result
            else:
                row = Stock(code=stock['code'], name=stock['name'],
                            url=url_detail.format(stock['code']), rate=result)
            session.add(row)
    session.commit()


if __name__ == '__main__':
    # main()
    # get_list()
    update_stocks()
    # update_script()
