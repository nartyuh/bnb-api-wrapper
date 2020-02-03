import requests
import json
from datetime import datetime
import time
import pandas as pd
from pandas import DataFrame as df
import hmac
import hashlib
from interval_enum import Interval
from order_enum import Order

class BinanceClient:

    def __init__(self, api_key, api_secret):
        self.key  = api_key
        self.secret = api_secret
        self.base = 'https://api.binance.com'
        self.endpoint = {
            'klines': '/api/v1/klines',
            'price_ticker': '/api/v3/ticker/price',
            '24hr_ticker': '/api/v3/ticker/24hr',
            'historical_trade': '/api/v3/historicalTrades',            # recent trades on the market
            'order': '/api/v3/order',
            'test_order': '/api/v3/order/test',
            'open_order': '/api/v3/openOrders',                        # all open orders
            'all_order': '/api/v3/allOrders',                          # all orders: active, cancelled, filler
            'my_trade': '/api/v3/myTrades'                             # all trades for a specific symbol on the account
        }


    '''
    ***********************************************************
                        GET METHODS
    ***********************************************************
    '''


    '''
        return klines for a specified symbol
        @param
            required - symbol: str, interval: Interval
    '''
    def get_klines(self, symbol, interval):

        # specifying parameters for request body
        params = {
            'symbol': symbol,
            'interval': interval.value
        }
        # specifying url enpoint
        url = self.base + self.endpoint['klines']

        # get api response
        response = requests.get(url, params=params)
        # convert json to dict
        data = json.loads(response.text)

        # convert dict to data frame
        klines_df = df(data)

        # get open time and close time from klines_df
        o_timestamp_df = klines_df[0]      # open timestamp
        c_timestamp_df = klines_df[6]      # close timestamp

        # create empty arrays for formatted datetime
        o_time = []      # open time
        c_time = []      # close time
        
        # convert timestamps to datetime format
        for (o_timestamp, c_timestamp) in zip(o_timestamp_df, c_timestamp_df):
            o_time.append(datetime.fromtimestamp(int(o_timestamp/1000)))
            c_time.append(datetime.fromtimestamp(int(c_timestamp/1000)))

        # convert datetime to string datetime format for df
        o_timestamp_df = df(o_time)
        c_timestamp_df = df(c_time)

        # replacing the original timestamp with formatted datetime string
        klines_df[0] = o_timestamp_df
        klines_df[6] = c_timestamp_df

        # modifying dataframe
        klines_df.pop(11)
        klines_df.columns = ['openTime', 'open', 'high', 'low', 'close',
                             'volume', 'closeTime', 'quoteAssetVol',
                             'no. of trades', 'taker_buy_baseAssetVol',
                             'taker_buy_quoteAssetVol']
        return klines_df


    '''
        return current price
            1. for a symbol if symbol is specified
            2. for all symbols
        @param
            optional - symbol: str
    '''
    def get_price(self, symbol=None):
        
        # specifying parameters for request body
        params = {
            'symbol': symbol
        }

        # specifying url endpoint
        url = self.base + self.endpoint['price_ticker']
        
        # get api response
        response = requests.get(url, params=params)
        # convert json to dict
        data = json.loads(response.text)

        # convert dict to dataframe
        if isinstance(data, list):
            price_df = df(data)
        else:
            price_df = df([data])

        return price_df


    '''
        return 24 hour ticker
            1. for a symbol if symbol is specified
            2. for all symbols
        @param
            optional - symbol: str
    '''       
    def get_24hr_ticker(self, symbol=None):

        # specify parameters for request body
        params = {
            'symbol': symbol
        }
        # specifying url endpoint
        url = self.base + self.endpoint['24hr_ticker']

        # request api response
        response = requests.get(url, params=params)
        # convert json to dict
        data = json.loads(response.text)
        
        # convert dict to dataframe
        if isinstance(data, list):
            ticker_df = df(data)
        else:
            ticker_df = df([data])

        # get openTime and closeTime from ticker_df
        open_time_df = ticker_df['openTime']
        close_time_df = ticker_df['closeTime']

        # create new empty arrays for openTime and closeTime
        open_time = []
        close_time = []

        # convert timestamps to datetime format
        for (o, c) in zip(open_time_df, close_time_df):
            open_time.append(datetime.fromtimestamp(int(o/1000)))
            close_time.append(datetime.fromtimestamp(int(c/1000)))

        # convert timestamps to string format
        open_time_df = df(open_time)
        close_time_df = df(close_time)

        # replace timestamps in ticker_df with formatted timestamps
        ticker_df['openTime'] = open_time_df
        ticker_df['closeTime'] = close_time_df

        return ticker_df


    '''
        return list of historical trades
            1. start from a specific trade if tradeId is specified upto
               the specified amount of trade records
            2. most recent trades if tradeId is not specified
                a. most recent 500 trades if limit is not specified
                b. the amount of trades specified by limit
        @param
            required - symbol: str
            optional - limit: int, tradeId: long
    '''
    def get_historical_trade(self, symbol, limit=None, tradeId=None):

        # specifying parameter for request body
        params = {
            'symbol': symbol,
            'limit': limit,
            'fromId': tradeId
        }
        # specifying url endpoint
        url = self.base + self.endpoint['historical_trade']

        # request api response
        response = requests.get(url, params=params, headers={'X-MBX-APIKEY': self.key})
        data = json.loads(response.text)

        # convert dict to dataframe
        trade_df = df(data)
        if not trade_df.empty:
            # get time from trade_df
            time_df = trade_df['time']
            
            # make new empty array for time
            _time = []

            # convert timestamp to datetime format
            for t in time_df:
                _time.append(datetime.fromtimestamp(int(t/1000)))
            
            # convert timestamp to string format
            time_df = df(_time)

            # replace timestamp in trade_df with formatted timestamp
            trade_df['time'] = time_df 

        return trade_df


    '''
        get the status of an order
        @param 
            required - symbol: str, orderId: long
    '''
    def get_query_order(self, symbol, orderId):
        
        # specify parameters for request body
        params = {
            'symbol': symbol,
            'orderId': orderId,
            'timestamp': int(round(time.time()*1000))
        }
        # specify url endpoint
        url = self.base + self.endpoint['order']
        
        # sign request
        self.sign_request(params)

        # request api response
        response = requests.get(url, params=params, headers={'X-MBX-APIKEY': self.key})
        data = json.loads(response.text)

        return data


    '''
        return list of open orders
            1. of a symbol if symbol is specified
            2. of all symbols if symbol is not specified
        @param 
            optional - symbol: str
    '''
    def get_open_order(self, symbol=None):

        # specify general paramenters for request body
        params = {
            'timestamp': int(round(time.time()*1000))

        }
        # specify optional parameters for request body
        if symbol != None:
            params['symbol'] = symbol
        # specify url endpoint
        url = self.base + self.endpoint['open_order']

        # sign request
        self.sign_request(params)

        # request api response
        response = requests.get(url, params=params, headers={'X-MBX-APIKEY': self.key})
        # convert json to dict
        data = json.loads(response.text)
        
        # convert dict to dataframe
        open_order_df = df(data)

        # if dataframe is not empty
        if not open_order_df.empty:
            # get time and updateTime form open_order_df
            time_df = open_order_df['time']                    # time
            updateTime_df = open_order_df['updateTime']        # updateTime

            # create new empty arrays for time and updateTime
            _time = []
            _updateTime = []

            # convert time and updateTime to datetime format
            for (t, u) in zip(time_df, updateTime_df):
                _time.append(datetime.fromtimestamp(int(t/1000)))
                _updateTime.append(datetime.fromtimestamp(int(u/1000)))

            # convert time and updateTime to df
            time_df = df(_time)
            updateTime_df = df(_updateTime)

            # replace original timestamps with formatted timestamps in open_order_df
            open_order_df['time'] = time_df
            open_order_df['updateTime'] = updateTime_df

        return open_order_df


    '''
        return all orders of the specified symbol: active, canceled, filled
            1. if orderId is specified, return orders with id >= orderId
            2. else, return most recent orders for this symbol 
        @param 
            required - symbol: str
            optional - orderId: long, limit: int
    '''
    def get_all_order(self, symbol, orderId=None, limit=None):

        # specify the general parameters for request body
        params = {
            'symbol': symbol,
            'timestamp': int(round(time.time()*1000))

        }
        # specify optional parameters for request body
        if limit != None:
            if orderId != None:
                params['orderId'] = orderId
                params['limit'] = limit
            else:
                params['limit'] = limit 
        else:
            if orderId != None:
                params['orderId'] = orderId
        # specify url endpoint
        url = self.base + self.endpoint['all_order']

        # sign request
        self.sign_request(params)

        # request api response
        response = requests.get(url, params=params, headers={'X-MBX-APIKEY': self.key})
        # convert json to dict
        data = json.loads(response.text)

        # convert data to dataframe
        all_order_df = df(data)

        # time and updateTime from all_order_df
        time_df = all_order_df['time']                    # time
        updateTime_df = all_order_df['updateTime']        # updateTime

        # create new empty arrays for time and updateTime
        _time = []
        _updateTime = []

        # convert time and updateTime to datetime format
        for (t, u) in zip(time_df, updateTime_df):
            _time.append(datetime.fromtimestamp(int(t/1000)))
            _updateTime.append(datetime.fromtimestamp(int(u/1000)))

        # convert time and updateTime to df
        time_df = df(_time)
        updateTime_df = df(_updateTime)

        # replace original timestamps with formatted timestamps in all_order_df
        all_order_df['time'] = time_df
        all_order_df['updateTime'] = updateTime_df

        return all_order_df

    
    '''
    ***********************************************************
                        POST METHODS
    ***********************************************************
    '''


    '''
        make a new order
            1. set test=True if want to test order
            2. set test=False if want to place order and the order is relected on the account
        @private
        @params 
            required - symbol: str, side: enum, orderType: enum
    '''
    def __new_order(self, symbol, side, orderType, test=True, timeInForce=None, quantity=None,
            quoteOrderQty=None, price=None, stopPrice=None, icebergQty=None):
        
        # specify the general parameters for request body
        params = {
            'symbol': symbol,
            'side': side.value,
            'type': orderType.value,
            'newOrderRespType': 'RESULT',
            'timestamp': int(round(time.time()*1000))
        }
        # specify option parameters for request body
        if orderType == Order.LIMIT:
            params['timeInForce'] = timeInForce
            params['quantity'] = quantity
            params['price'] = price
            if icebergQty != None:
                params['icebergQty'] = icebergQty
        elif orderType == Order.MARKET:
            params['quantity'] = quantity
        elif orderType == Order.STOP_LOSS:
            params['quantity'] = quantity
            params['stopPrice'] = stopPrice 
        elif orderType == Order.STOP_LOSS_LIMIT:
            params['timeInForce'] = timeInForce
            params['quantity'] = quantity
            params['price'] = price
            params['stopPrice'] = stopPrice
            if icebergQty != None:
                params['icebergQty'] = icebergQty
        elif orderType == Order.TAKE_PROFIT:
            params['quantity'] = quantity
            params['stopPrice'] = stopPrice
        elif orderType == Order.TAKE_PROFIT_LIMIT:
            params['timeInForce'] = timeInForce
            params['quantity'] = quantity
            params['price'] = price
            params['stopPrice'] = stopPrice
            if icebergQty != None:
                params['icebergQty'] = icebergQty
        elif orderType == Order.LIMIT_MAKER:
            params['quantity'] = quantity
            params['price'] = price
        else:
            raise Exception('Invalid order type.')
        # specify url endpoint
        if test == True:
            url = self.base + self.endpoint['test_order']
        else:
            url = self.base + self.endpoint['order']

        # sign request
        self.sign_request(params)

        # initialize new order, request api response
        try:
            response = requests.post(url, params=params, headers={'X-MBX-APIKEY': self.key})
            data = json.loads(response.text)
        except Exception as e:
            print('Exception occured when trying to place buy order.')
            data = json.loads(e.text)

        return data

    '''
       make a new buy order 
            1. set test=True if want to test buy order
            2. set test=False if want to place buy order and the buy order is relected on the account
       @params 
            required - symbol: str, orderType: enum
    '''
    def buy(self, symbol, orderType, test=True, timeInForce=None, quantity=None,
            quoteOrderQty=None, price=None, stopPrice=None, icebergQty=None):

        return self.__new_order(symbol, Order.BUY, orderType, test=test, timeInForce=timeInForce, quantity=quantity,
                                quoteOrderQty=quoteOrderQty, price=price, stopPrice=stopPrice, icebergQty=icebergQty)
    

    '''
        make a new sell order
            1. set test=True if want to test sell order
            2. set test=False if want to place sell order and the sell order is relected on the account
        @params 
            required - symbol: str, orderType: enum
    '''
    def sell(self, symbol, orderType, test=True, timeInForce=None, quantity=None,
            quoteOrderQty=None, price=None, stopPrice=None, icebergQty=None):
        
        return self.__new_order(symbol, Order.SELL, orderType, test=test, timeInForce=timeInForce, quantity=quantity,
                                quoteOrderQty=quoteOrderQty, price=price, stopPrice=stopPrice, icebergQty=icebergQty)

    
    '''
    ***********************************************************
                        DELETE METHODS
    ***********************************************************
    '''


    '''
        cancel an open order
    '''
    def cancel_order(self, symbol, orderId):

        # specify parameters for request body
        params = {
            'symbol': symbol,
            'orderId': orderId,
            'timestamp': int(round(time.time()*1000))
        }
        # specify url endpoint
        url = self.base + self.endpoint['order']

        # sign request
        self.sign_request(params)

        # initialize cancel order, request api response
        try:
            response = requests.delete(url, params=params, headers={'X-MBX-APIKEY': self.key})
            data = json.loads(response.text)
        except Exception as e:
            print('Failed to cancel order with ID' + orderId)
            data = json.loads(e.text)
        
        return data


    '''
        sign your request to Binance API
    '''
    def sign_request(self, params: dict):
        
        #make a query string
        query_string = '&'.join(["{}={}".format(d,params[d]) for d in params])
        
        #hashing secret
        signature = hmac.new(self.secret.encode('utf-8'), 
                             query_string.encode('utf-8'),
                             hashlib.sha256)
        
        # add your signature to the request body
        params['signature'] = signature.hexdigest()

