import requests
import json
import pandas as pd
import hmac

class Client:
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
            'open_order': '/api/v3/openOrders',          # all open orders
            'all_order': '/api/v3/allOrders',            # all orders: active, cancelled, filler
            'my_trade': '/api/v3/myTrades',              # all trades for a specific symbol on the account
            'recent_trade': '/api/v3/trades'             # recent trades on the market
        }



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
    
