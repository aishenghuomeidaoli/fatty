# _*_ coding: utf-8 _*_
from __future__ import absolute_import, unicode_literals

import time
import logging
import tushare as ts

from celery import shared_task
from requests import Request, Session

from stock.models import Stock, StockKDay

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


@shared_task
def update_stock_k_day():
    stocks = Stock.objects.all()
    for stock in stocks:
        code = stock.code
        if not code.isdigit():
            continue
        ds = ts.get_hist_data(code)
        ds = ds.T.to_dict()
        for date, data in ds.iteritems():
            open_price = data.get('open')
            close = data.get('close')
            low = data.get('low')
            high = data.get('high')
            price_change = data.get('price_change')
            p_change = data.get('p_change')
            volume = data.get('volume')
            ma5 = data.get('ma5')
            ma10 = data.get('ma10')
            ma20 = data.get('ma20')
            StockKDay.objects.update_or_create(code=code, date=date, defaults={
                'stock_id': stock.id,
                'open': open_price,
                'close': close,
                'low': low,
                'high': high,
                'price_change': price_change,
                'p_change': p_change,
                'volume': volume,
                'ma5': ma5,
                'ma10': ma10,
                'ma20': ma20
            })

if __name__ == '__main__':
    # main()
    # get_list()
    update_stocks()
    # update_script()
