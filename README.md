# Binance API Client
 
## Binance API documentation
  To read more about Binance API, go to: https://binance-docs.github.io/apidocs/
  
## Note

***This is an unofficial Binance API wrapper written in Python. This is in no way affliated with Binance in under any circumstances. Please use at your own risk.***

## Features

Supported functions:
* get_klines()
* get_price()
* get_24_hr_ticker()
* get_historical_trade()
* get_open_order()
* get_all_order()

## How to install

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

## Quickstart

```
client = BinanceClient('your-api-key', 'your-api-secret')
```
