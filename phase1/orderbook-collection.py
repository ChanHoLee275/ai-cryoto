from datetime import datetime
from apscheduler.schedulers.background import BlockingScheduler
import requests
import os

log = open('log.txt', 'a')

def timestamp_to_date(timestamp):
    date  = datetime.fromtimestamp(int(timestamp))
    return str(date)

def request_order_book():
    try:
        res = requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=15')
    except:
        log.write("NetworkError!\n")
    return res.json()

def is_validate_response(res: requests.Response):
    keys = res['data'].keys()
    for i in ['timestamp', 'payment_currency', 'order_currency', 'bids', 'asks']:
        if not (i in keys):
            return False
    if len(res['data']['bids']) != 15 or len(res['data']['asks']) != 15:
        return False
    return True

def create_orderbook(level=15, res={}, timestamp=0):
    sortedBids = sorted(res['data']['bids'], key=lambda order: order['price'])[0:level-1]
    sortedAsks = sorted(res['data']['asks'], key=lambda order: order['price'])[0:level-1]
    order_book_bids = list(map(lambda x: x['price'] + ',' + "{:.6f}".format(float(x['quantity'])) + ',' + '1,' + timestamp_to_date(timestamp) ,sortedBids))
    order_book_asks = list(map(lambda x: x['price'] + ',' + "{:.6f}".format(float(x['quantity'])) + ',' + '0,' + timestamp_to_date(timestamp) ,sortedAsks))
    return {'bids': order_book_bids, 'asks': order_book_asks}

def create_csv_file(filename):
    fs = open(filename, 'a')
    fs.write("price,quantity,type,timestamp\n")
    fs.close()
    return 0

def write_csv(orderbooks={}, timestamp=0):
	# write order book in file
    date = datetime.fromtimestamp(int(timestamp))
    filename = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '-bithumb-btc-orderbook.csv'
    if not os.path.exists(filename):
        create_csv_file(filename)
    fs = open(filename, 'a')
    results = list(reversed(orderbooks['asks'])) + list(reversed(orderbooks['bids']))
    for i in results:
        fs.write(i + '\n')
    return 0

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=1, id='save_data')
def main():
    current_time = datetime.now().timestamp()
    res = request_order_book()
    if not is_validate_response(res) or res['status'] != "0000":
        log.write("invalid response : " + timestamp_to_date(current_time))
        return False
    order_book = create_orderbook(res = res, timestamp=current_time)
    write_csv(order_book, current_time)
    return True

scheduler.start()
