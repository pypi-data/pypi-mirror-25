__author__ = 'kmadac'

import os
import bitstamp.client
import time


trading_client = bitstamp.client.Trading(username='999999', key='xxx', secret='xxx')
print(trading_client.account_balance()['fee'])
print(trading_client.ticker()['volume'])   # Can access public methods

