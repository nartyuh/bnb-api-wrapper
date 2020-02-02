from bnb_wrapper import BinanceClient
from interval_enums import Interval

bnb = BinanceClient('MYFPFEYF2zfmnLxZODGqGckY7zWlGHYkA2Zgkege8APEIjHKhrRXtcMW1hILDi3v', 
                    'AIxfhSQ53qZA5zvJsOglp71IDm7Ccq3kPwv98d1eM7FzIkKUBfmjImkvQSolGcZq')

print('--------------------------------------------------------------------------------------------')
print(bnb.get_klines('BNBBTC', Interval._5MINUTE))

print('--------------------------------------------------------------------------------------------')
print(bnb.get_price())
print(bnb.get_price(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print(bnb.get_24hr_ticker())
print(bnb.get_24hr_ticker(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print(bnb.get_historical_trade('BNBBTC'))
print(bnb.get_historical_trade('BNBBTC', limit=1000))
print(bnb.get_historical_trade('BNBBTC', limit=1, tradeId=69010498))

print('--------------------------------------------------------------------------------------------')
print(bnb.get_query_order('LTCBTC', orderId=1))

print('--------------------------------------------------------------------------------------------')
print(bnb.get_open_order())
print(bnb.get_open_order(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print(bnb.get_all_order('LINKUSDT'))
print(bnb.get_all_order('LINKUSDT', orderId=48851949))
print(bnb.get_all_order('LINKUSDT', limit=1000))
print(bnb.get_all_order('LINKUSDT', orderId=48851949, limit=1000))

