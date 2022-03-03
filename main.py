from msilib.schema import Feature
from random import triangular
import ccxt
import config
import json
import datetime
from client import FtxWebsocketClient
from websocket_manager import WebsocketManager
from time import sleep
from triangular_arbitrage import TriangularArbitrage
ftx = ccxt.ftx({
    'apiKey': config.FTXAPIKey,
    'secret': config.FTXSecretKey

})


def get_quote(request):
    # markets = ftx.load_markets()
    symbol = request.args.get('symbol')
    try:
        quote = ftx.fetch_ticker(symbol)
    except Exception as e:
        return {
            "code": "error",
            "message": str(e)
        }
    return quote


def trade_crypto(request):
    data = request.get_json()
    order = ftx.create_market_buy_order(data['symbol'], data['quantity'])
    return order


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


time = get_timestamp()

if __name__ == '__main__':
    client_manager = WebsocketManager()
    client = FtxWebsocketClient()
    triangular_arbitrage = TriangularArbitrage()
    FEE = 0.0007
    symbols = ['DOT', 'LTC', 'ETH', 'UNI', 'WBTC', 'SOL', 'XRP', 'FTT', 'AVAX',
               'BNB', 'DOGE', 'LINK', 'SUSHI', 'MATIC', 'YFI', 'BCH', 'TRX', 'CEL', 'SXP']
    list_revenue = {}

    # {'DOT':(ask,bid),'LTC':(ask,bid)}
    while(True):
        for x in symbols:
            list_revenue[x] = triangular_arbitrage.find_arbitrage(x, client)
        list_revenue_bid = dict(
            sorted(list_revenue.items(), key=lambda item: item[1][0], reverse=True))
        list_revenue_ask = dict(
            sorted(list_revenue.items(), key=lambda item: item[1][1], reverse=True))
        for x in list(list_revenue_bid.items())[:3]:
            print('bid: ' + str(x[0])+": "+str(x[1][0]*100))
        print('=====================')
        for x in list(list_revenue_ask.items())[:3]:
            print('ask: '+str(x[0])+": "+str(x[1][1]*100))
        print('=====================')

        # trades = client.get_trades('UNI/USD')
        # orderbook_uni_usd = client.get_orderbook('UNI/USD')
        # orderbook_uni_btc = client.get_orderbook('UNI/BTC')
        # orderbook_btc_usd = client.get_orderbook('BTC/USD')
        # print('=====================')
        # if len(trades) != 0:
        #     print(trades[0])
        # two_product_bid = orderbook_btc_usd['bids'][0][0] * \
        #     orderbook_uni_btc['bids'][0][0]
        # two_product_ask = orderbook_btc_usd['asks'][0][0] * \
        #     orderbook_uni_btc['asks'][0][0]
        # uni_price = orderbook_uni_usd['bids'][0][0]/two_product_ask
        # uni_price_with_fee = uni_price*(1-FEE)-(1+FEE)

        # uni_price_2 = two_product_bid/orderbook_uni_usd['asks'][0][0]
        # uni_price_with_fee_2 = uni_price_2*(1-FEE)-(1+FEE)
        # profit = orderbook_uni_usd['bids'][0][0]*(1-FEE)/orderbook_uni_btc['asks'][0][0]-orderbook_btc_usd['asks'][0][0]*(1+FEE)
        # profit_nofee = orderbook_uni_usd['bids'][0][0]/orderbook_uni_btc['asks'][0][0]-orderbook_btc_usd['asks'][0][0]
        # print(str(profit/orderbook_btc_usd['asks'][0][0]*100)+'%')
        # print(str(profit_nofee/orderbook_btc_usd['asks'][0][0]*100)+'%')
        # print(uni_price_with_fee_2)
        # print(uni_price_2-1)
        # print(uni_price_with_fee)
        # print(uni_price-1)
        # print('BTC/USD: '+str(orderbook_btc_usd['asks'][0][0]))
        # print('UNI/BTC: '+str(orderbook_uni_btc['asks'][0][0]))
        # print('UNI/USD: '+str(orderbook_uni_usd['bids'][0][0]))
        # print('bids: ' + str(orderbook_uni_usd['bids'][0]))
        # print('asks: '+str(orderbook_uni_usd['asks'][0]))
        sleep(0.5)
    # for x in ret:
    #     print(x['asks'])
