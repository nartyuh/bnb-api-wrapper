from binance import BinanceClient
from interval_enum import Interval
from order_enum import Order

# Don't tryna steal cuz they won't work
bnb = BinanceClient('', '')

print('--------------------------------------------------------------------------------------------')
print('TEST getKlines')
print(bnb.getKlines('BNBBTC', Interval._5MINUTE))

print('--------------------------------------------------------------------------------------------')
print('TEST getPrice')
print(bnb.getPrice())
print(bnb.getPrice(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print('TEST get24hrTicker')
print(bnb.get24hrTicker())
print(bnb.get24hrTicker(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print('TEST getHistoricalTrade')
print(bnb.getHistoricalTrade('BNBBTC'))
print(bnb.getHistoricalTrade('BNBBTC', limit=1000))
print(bnb.getHistoricalTrade('BNBBTC', limit=10, tradeId=69010498))
print(bnb.getHistoricalTrade('BNBBTC', limit=0, tradeId=69010498))

print('--------------------------------------------------------------------------------------------')
print('TEST getqueryOrder')
print(bnb.getQueryOrder('LINKUSDT', orderId=120218697))

print('--------------------------------------------------------------------------------------------')
print('TEST getOpenOrder')
print(bnb.getOpenOrders())
print(bnb.getOpenOrders(symbol='BNBBTC'))

print('--------------------------------------------------------------------------------------------')
print('TEST getAllOrder')
print(bnb.getAllOrdersBySymbol('LINKUSDT'))
print(bnb.getAllOrdersBySymbol('LINKUSDT', orderId=48851949))
print(bnb.getAllOrdersBySymbol('LINKUSDT', limit=1000))
print(bnb.getAllOrdersBySymbol('LINKUSDT', orderId=48851949, limit=1000))

print('--------------------------------------------------------------------------------------------')
print('TEST buy/sell')
print(bnb.sell('LINKUSDT', orderType=Order.MARKET, quantity=10))
print(bnb.buy('LINKUSDT', orderType=Order.MARKET, quantity=9.9))

print('--------------------------------------------------------------------------------------------')
print('TEST cancelOrder')
print(bnb.cancelOrder('LINKUSDT', orderId=120218697))
