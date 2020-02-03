from binance import BinanceClient
from interval_enum import Interval
from order_enum import Order

# Don't tryna steal cuz they won't work
bnb = BinanceClient('MYFPFEYF2zfmnLxZODGqGckY7zWlGHYkA2Zgkege8APEIjHKhrRXtcMW1hILDi3v', 
                    'AIxfhSQ53qZA5zvJsOglp71IDm7Ccq3kPwv98d1eM7FzIkKUBfmjImkvQSolGcZq')

print('--------------------------------------------------------------------------------------------')
print('TEST get_klines')
print(bnb.get_klines('BNBBTC', Interval._5MINUTE))

print('--------------------------------------------------------------------------------------------')
print('TEST get_price')
print(bnb.get_price())
print(bnb.get_price(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print('TEST get_24hr_ticker')
print(bnb.get_24hr_ticker())
print(bnb.get_24hr_ticker(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print('TEST get_historical_trade')
print(bnb.get_historical_trade('BNBBTC'))
print(bnb.get_historical_trade('BNBBTC', limit=1000))
print(bnb.get_historical_trade('BNBBTC', limit=10, tradeId=69010498))
print(bnb.get_historical_trade('BNBBTC', limit=0, tradeId=69010498))

print('--------------------------------------------------------------------------------------------')
print('TEST get_query_order')
print(bnb.get_query_order('LINKUSDT', orderId=120218697))

print('--------------------------------------------------------------------------------------------')
print('TEST get_open_order')
print(bnb.get_open_order())
print(bnb.get_open_order(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print('TEST get_all_order')
print(bnb.get_all_order('LINKUSDT'))
print(bnb.get_all_order('LINKUSDT', orderId=48851949))
print(bnb.get_all_order('LINKUSDT', limit=1000))
print(bnb.get_all_order('LINKUSDT', orderId=48851949, limit=1000))

print('--------------------------------------------------------------------------------------------')
print('TEST buy/sell')
print(bnb.sell('LINKUSDT', orderType=Order.MARKET, quantity=10))
print(bnb.buy('LINKUSDT', orderType=Order.MARKET, quantity=9.9))

print('--------------------------------------------------------------------------------------------')
print('TEST cancel_order')
print(bnb.cancel_order('LINKUSDT', orderId=120218697))