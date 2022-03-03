from msilib.schema import Feature
from random import triangular
import ccxt
import config
import json
import datetime
from wsclient.client import FtxWebsocketClient
from wsclient.websocket_manager import WebsocketManager
from time import sleep
from triangular_arbitrage import TriangularArbitrage
from rest.FtxClient import FtxClient
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
    ftx_client = FtxClient()
    triangular_arbitrage.trading(100,client_manager,client,ftx_client)

