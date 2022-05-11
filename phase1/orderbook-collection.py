import requests

def request_order_book():
    res = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=15')
    return res.json()