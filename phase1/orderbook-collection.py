from datetime import datetime
import requests

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
