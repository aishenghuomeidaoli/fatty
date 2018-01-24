# _*_ coding: utf-8 _*_
import time
import datetime
from requests import Request, Session
# import constant
# from models import Stock, session

url_all = 'https://xueqiu.com/stock/cata/stocklist.json?page={page}&size=90&order=desc&orderby=code&type=11%2C12&_={now}'

url_detail = 'https://xueqiu.com/S/{}'
url_stat = 'https://xueqiu.com/v4/stock/quote.json?code={0}&_={1}'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'host': 'xueqiu.com',
}

s = Session()
s.get('https://xueqiu.com/', headers=headers)


def http(request):
    prepared = s.prepare_request(request)
    resp = s.send(prepared)
    return resp.json()


def get_list():
    for page in range(1, 60):
        url = url_all.format(**{'page': page, 'now': int(time.time() * 1000)})
        r = Request('GET', url, headers=headers)
        data = http(r)
        print data, '-----'
        stocks = data['stocks']
        for stock in stocks:
            print "    {'code': '%s', 'name': u'%s', 'current': '%s'}," % (stock['symbol'], stock['name'], stock['current'])
    return


def judge(code):
    """判断是否为上吊线

    :param code:
    :return:
    """
    url = url_stat.format(code, int(time.time() * 1000))
    r = Request('GET', url, headers=headers)
    data = http(r).values()[0]
    start, end, high, low = float(data['open']), float(data['current']), float(data['high']), float(data['low'])
    range_rise = abs(start - end)
    range_wave = abs(high - low)
    if range_rise != 0 and 3 * range_rise < range_wave:
        return int(range_wave/range_rise)
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
                data[result] = [{'name': stock['name'], 'url': url_detail.format(stock['code'])}]
            else:
                data[result].append({'name': stock['name'], 'url': url_detail.format(stock['code'])})
    return data


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
            row = session.query(Stock).filter_by(code=stock['code'], date=datetime.datetime.now().date()).first()
            if row:
                row.rate = result
            else:
                row = Stock(code=stock['code'], name=stock['name'], url=url_detail.format(stock['code']), rate=result)
            session.add(row)
    session.commit()

if __name__ == '__main__':
    # main()
    get_list()
    # update_script()
