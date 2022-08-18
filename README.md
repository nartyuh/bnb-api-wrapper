# Binance API Client

## Binance API documentation

  To read more about Binance API, go to: <https://binance-docs.github.io/apidocs/>
  
## Note

***This is an unofficial Binance API wrapper written in Python. This is in no way affliated with Binance in under any circumstances. Please use at your own risk.***

## How to install (deprecated due to no longer available on PyPI)

**To install:**

```
pip install binanceAPI-abr-ver
```

**to import the package:**

```
from binance.binance import BinanceClient
from binance.interval_num import Interval
from binance.order_num import Order
```

## Get started

```
client = BinanceClient('your-api-key', 'your-api-secret')
```

## Supported functions

### `getKlines`

```
return klines for a specified symbol
@param
  required - symbol: str, interval: Interval
```

### `getPrice`

```
return current price
  1. for a symbol if symbol is specified
  2. for all symbols
@param
  optional - symbol: str
```

### `get24hrTicker`

```
return 24 hour ticker
  1. for a symbol if symbol is specified
  2. for all symbols
@param
  optional - symbol: str
```

### `getHistoricalTrade`

```
return list of historical trades
  1. start from a specific trade if tradeId is specified upto the specified amount of trade records
  2. most recent trades if tradeId is not specified
    a. most recent 500 trades if limit is not specified
    b. the amount of trades specified by limit
@param
  required - symbol: str
  optional - limit: int, tradeId: long
```

### `getOrderStatus`

```
get the status of an order
@param 
  required - symbol: str, orderId: long
```

### `getOpenOrders`

```
return list of open orders
  1. of a symbol if symbol is specified
  2. of all symbols if symbol is not specified
@param 
  optional - symbol: str
```

### `getAllOrdersBySymbol`

```
return all orders of the specified symbol: active, canceled, filled
  1. if orderId is specified, return orders with id >= orderId
  2. else, return most recent orders for this symbol 
@param 
  required - symbol: str
  optional - orderId: long, limit: int
```

### `buy`

```
make a new buy order 
  1. set test=True if want to test buy order
  2. set test=False if want to place buy order and the buy order is relected on the account
@params 
  required - symbol: str, orderType: enum
```

### `sell`

```
make a new sell order
  1. set test=True if want to test sell order
  2. set test=False if want to place sell order and the sell order is relected on the account
@params 
  required - symbol: str, orderType: enum
```

### `cancelOrder`

```
cancel an open order
@param
  require symbol: str, orderId: long
```
