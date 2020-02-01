import requests
import json
from datetime import datetime
import pandas as pd
from pandas import DataFrame as df
import hmac
from interval_enums import Interval

class BinanceClient:
    BASE_URL = 'https:/api.binance.com'
    #endpoint = ''
    #params = request_body
    

    def __init__(self, api_key: str, api_secret: str):
        self.key  = api_key
        self.secret = api_secret
        self.base = 'https://api.binance.com'
        self.endpoint = {
            'klines': '/api/v1/klines',
            'price_ticker': '/api/v3/ticker/price',
            '24hr_ticker': '/api/v3/ticker/24hr',
            'order': '/api/v3/order',
            'test_order': '/api/v3/order/test',
            'open_order': '/api/v3/openOrders',          # all open orders
            'all_order': '/api/v3/allOrders',            # all orders: active, cancelled, filler
            'my_trade': '/api/v3/myTrades',              # all trades for a specific symbol on the account
            'recent_trade': '/api/v3/trades'             # recent trades on the market
        }

    '''
        return klines for a specified symbol
    '''
    def get_klines(self, symbol: str, interval: Interval):

        # specifying params for request body
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
        
        # delete later
        # print(data)

        # convert dict to data frame
        klines_df = df(data)

        # delete later
        # print(klines_df)

        # get open time and close time from klines_df
        o_timestamp_df = klines_df[0]      # open timestamp
        c_timestamp_df = klines_df[6]      # close timestamp

        # delete later
        # print(o_timestamp_df)
        # print(c_timestamp_df)

        # create empty arrays for formatted datetime
        o_time = []      # open time
        c_time = []      # close time
        
        # convert timestamps to datetime format
        for (o_timestamp, c_timestamp) in zip(o_timestamp_df, c_timestamp_df):
            o_time.append(datetime.fromtimestamp(int(o_timestamp/1000)))
            c_time.append(datetime.fromtimestamp(int(c_timestamp/1000)))
        
        # delete later
        # print(o_time)
        # print(c_time)

        # convert datetime to string datetime format for df
        o_time_df = df(o_time)
        c_time_df = df(c_time)

        # delete later
        # print(o_time_df)
        # print(c_time_df)

        # replacing the original timestamp with formatted datetime string
        klines_df[0] = o_time_df
        klines_df[6] = c_time_df

        # delete later
        # print(klines_df)

        return klines_df

    '''
        return current price
            1. for a symbol if symbol is specified
            2. for all symbols
    '''
    def get_price(self, symbol = None):
        
        # specifying parameter for the request body
        params = {
            'symbol': symbol
        }

        # specifying url endpoint
        url = self.base + self.endpoint['price_ticker']
        
        # get api response
        response = requests.get(url, params=params)
        # convert json to dict
        data = json.loads(response.text)

        # delete later
        # print(data)

        # convert dict to dataframe
        price_df = df(data)

        # delete later
        # print(price_df)

        return price_df
        


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


bnb = BinanceClient('', '')

# bnb.get_klines('BNBBTC', Interval._5MINUTE)

# bnb.get_price()
