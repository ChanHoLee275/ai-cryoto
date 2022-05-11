import requests

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