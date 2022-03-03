from numpy import number, void
from wsclient.client import FtxWebsocketClient
from rest.FtxClient import FtxClient
from wsclient.client import FtxWebsocketClient
from wsclient.websocket_manager import WebsocketManager
import config
from time import sleep

class TriangularArbitrage:

    _USD = 'USD'
    _BTC = 'BTC'

    def __init__(self) -> None:
        pass

    @classmethod
    def find_arbitrage(self, name: str, client: FtxWebsocketClient, 
    fee: number = 0.0007, is_market_order: bool = True) -> tuple():
        btc_usd = self._BTC+'/'+self._USD
        symbol_usd = name+'/'+self._USD
        symbol_btc = name+'/'+self._BTC

        orderbook_symbol_usd = client.get_orderbook(symbol_usd)
        orderbook_symbol_btc = client.get_orderbook(symbol_btc)
        orderbook_btc_usd = client.get_orderbook(btc_usd)

        
        if(is_market_order):
            # sell
            # bid bid ask
            two_product_bid = orderbook_btc_usd['bids'][0][0] * \
                orderbook_symbol_btc['bids'][0][0]
            symbol_price_bid = two_product_bid / \
                orderbook_symbol_usd['asks'][0][0]
            symbol_price_bid_with_fee=(symbol_price_bid*(1-fee)-(1+fee),orderbook_btc_usd['bids'][0][0],orderbook_symbol_btc['bids'][0][0], orderbook_symbol_usd['asks'][0][0])

            #buy
            # ask ask bid
            two_product_ask = orderbook_btc_usd['asks'][0][0] * \
                orderbook_symbol_btc['asks'][0][0]
            symbol_price_ask = orderbook_symbol_usd['bids'][0][0] / \
                two_product_ask
            symbol_price_ask_with_fee=(symbol_price_ask*(1-fee)-(1+fee),orderbook_btc_usd['asks'][0][0],orderbook_symbol_btc['asks'][0][0],orderbook_symbol_usd['bids'][0][0])
        else:
            # sell
            # bid bid ask
            two_product_bid = orderbook_btc_usd['asks'][0][0] * \
                orderbook_symbol_btc['asks'][0][0]
            symbol_price_bid = two_product_bid / \
                orderbook_symbol_usd['bids'][0][0]
            symbol_price_bid_with_fee=(symbol_price_bid*(1-fee)-(1+fee),orderbook_btc_usd['asks'][0][0],orderbook_symbol_btc['asks'][0][0], orderbook_symbol_usd['bids'][0][0])

            # buy
            # ask ask bid
            two_product_ask = orderbook_btc_usd['bids'][0][0] * \
                orderbook_symbol_btc['bids'][0][0]
            symbol_price_ask = orderbook_symbol_usd['asks'][0][0] / \
                two_product_ask
            symbol_price_ask_with_fee=(symbol_price_ask*(1-fee)-(1+fee),orderbook_btc_usd['bids'][0][0],orderbook_symbol_btc['bids'][0][0],orderbook_symbol_usd['asks'][0][0])
        return (symbol_price_bid_with_fee, symbol_price_ask_with_fee)

    @classmethod
    def place_order(self, name: str,client: FtxClient,side:str,investment:number)->void:
        price = 0
        size = investment/price

        res = client.place_order(name,side,price,size,'limit',False,False,True)
        print(res)
        return
    
    def trading(self,investment:number,client_manager:WebsocketManager,client:FtxWebsocketClient,ftx_client:FtxClient):
          

        list_revenue = {}

        # {'DOT':(ask,bid),'LTC':(ask,bid)}
        while(True):
            for x in config.SYMBOLS:
                list_revenue[x] = self.find_arbitrage(x, client,0.0002,False)
            list_revenue_bid = dict(
                sorted(list_revenue.items(), key=lambda item: item[1][0][0], reverse=True))
            list_revenue_ask = dict(
                sorted(list_revenue.items(), key=lambda item: item[1][1][1], reverse=True))
            for x in list(list_revenue_bid.items())[:3]:
                print('bid: ' + str(x[0])+": "+str(x[1][0][0]*100))
                # if(x[1][0]>0):
                #     self.place_order(x[0]+'/USD',ftx_client,'buy',investment)
                
            print('=====================')
            for x in list(list_revenue_ask.items())[:3]:
                print('ask: '+str(x[0])+": "+str(x[1][1][0]*100))
            print('=====================')

            sleep(0.5)


        return 