from datetime import datetime
import requests
import os

def timestamp_to_date(timestamp):
    date  = datetime.fromtimestamp(int(timestamp)/1000)
    return str(date)

def request_order_book():
    res = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=15')
    return res.json()

def is_validate_response(res: requests.Response):
    keys = res['data'].keys()
    for i in ['timestamp', 'payment_currency', 'order_currency', 'bids', 'asks']:
        if not (i in keys):
            return False
    if len(res['data']['bids']) != 15 or len(res['data']['asks']) != 15:
        return False
    return True

def create_orderbook(level=15, res={}):
    sortedBids = sorted(res['data']['bids'], key=lambda order: order['price'])[0:level-1]
    sortedAsks = sorted(res['data']['asks'], key=lambda order: order['price'])[0:level-1]
    order_book_bids = list(map(lambda x: x['price'] + ',' + "{:.6f}".format(float(x['quantity'])) + ',' + '1,' + timestamp_to_date(res['data']['timestamp']) ,sortedBids))
    order_book_asks = list(map(lambda x: x['price'] + ',' + "{:.6f}".format(float(x['quantity'])) + ',' + '0,' + timestamp_to_date(res['data']['timestamp']) ,sortedAsks))
    return {'bids': order_book_bids, 'asks': order_book_asks}

def create_csv_file(filename):
    fs = open(filename, 'a')
    fs.write("price,quantity,type,timestamp\n")
    fs.close()
    return 0

def write_csv(orderbooks={}):
	# write order book in file
    date = datetime.now()
    filename = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '-bithumb-btc-orderbook.csv'
    if not os.path.exists(filename):
        create_csv_file(filename)
    fs = open(filename, 'a')
    results = list(reversed(orderbooks['asks'])) + list(reversed(orderbooks['bids']))
    for i in results:
        fs.write(i + '\n')
    return 0