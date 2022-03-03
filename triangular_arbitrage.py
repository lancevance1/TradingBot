from numpy import number
from client import FtxWebsocketClient


class TriangularArbitrage:

    _USD = 'USD'
    _BTC = 'BTC'

    def __init__(self) -> None:
        pass

    @classmethod
    def find_arbitrage(self, name: str, client: FtxWebsocketClient, fee: number = 0.0007, is_market_order: bool = True) -> tuple():
        btc_usd = self._BTC+'/'+self._USD
        symbol_usd = name+'/'+self._USD
        symbol_btc = name+'/'+self._BTC

        orderbook_symbol_usd = client.get_orderbook(symbol_usd)
        orderbook_symbol_btc = client.get_orderbook(symbol_btc)
        orderbook_btc_usd = client.get_orderbook(btc_usd)

        if(is_market_order):
            #bid bid ask
            two_product_bid = orderbook_btc_usd['bids'][0][0] * \
                orderbook_symbol_btc['bids'][0][0]
            symbol_price_bid = two_product_bid/orderbook_symbol_usd['asks'][0][0]
            symbol_price_bid_with_fee = symbol_price_bid*(1-fee)-(1+fee)

            # print('symbol_price_bid_with_fee: '+ str(symbol_price_bid_with_fee) )
            # print('symbol_price_bid: '+str(symbol_price_bid-1))
            #ask ask bid            
            two_product_ask = orderbook_btc_usd['asks'][0][0] * \
                orderbook_symbol_btc['asks'][0][0]
            symbol_price_ask = orderbook_symbol_usd['bids'][0][0]/two_product_ask
            symbol_price_ask_with_fee = symbol_price_ask*(1-fee)-(1+fee)

            # print('symbol_price_ask_with_fee: '+str(symbol_price_ask_with_fee))
            # print('symbol_price_ask:'+str(symbol_price_ask-1))


            # print(btc_usd+': '+str(orderbook_btc_usd['asks'][0][0]))
            # print(symbol_btc+': '+str(orderbook_symbol_btc['asks'][0][0]))
            # print(symbol_usd+': '+str(orderbook_symbol_usd['bids'][0][0]))
            # print('bids: ' + str(orderbook_symbol_usd['bids'][0]))
            # print('asks: '+str(orderbook_symbol_usd['asks'][0]))
            
            # print('=====================')
        return (symbol_price_bid_with_fee,symbol_price_ask_with_fee)
