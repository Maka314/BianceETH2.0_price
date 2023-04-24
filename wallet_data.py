from binance.spot import Spot
from binance.um_futures import UMFutures #U-based Perpetual Contract API
#from binance.cm_futures import CMFutures #Coin-based Perpetual Contract API

import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')
api_key, api_secret = config.get('biance_api', 'api_key'), config.get('biance_api', 'secret')
base_url = config.get('biance_api', 'base_url')

spot_client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)
future_client = UMFutures(key=api_key, secret=api_secret)

#Get the dividend record.
staking_record = pd.DataFrame(spot_client.asset_dividend_record(asset='BETH', limit=50)['rows'])
spot_client.account_snapshot(type='SPOT')

c_future_balance = pd.DataFrame(future_client.balance())
spot_client.ticker_price(symbol='BETHUSDT')
future_client.get_income_history()