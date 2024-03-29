from binance.spot import Spot
from binance.um_futures import UMFutures #U-based Perpetual Contract API
#from binance.cm_futures import CMFutures #Coin-based Perpetual Contract API

import configparser
import pandas as pd
import datetime

config = configparser.ConfigParser()
config.read('config.ini')
api_key, api_secret = config.get('biance_api', 'api_key'), config.get('biance_api', 'secret')
base_url = config.get('biance_api', 'base_url')
nv_file = config.get('local_setting', 'nv_log')

spot_client = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)
future_client = UMFutures(key=api_key, secret=api_secret)

'''
#Get the dividend record.
staking_record = pd.DataFrame(spot_client.asset_dividend_record(asset='BETH', limit=50)['rows'])
spot_client.account_snapshot(type='SPOT')

c_future_balance = pd.DataFrame(future_client.balance())
spot_client.ticker_price(symbol='BETHUSDT')
future_client.get_income_history()
'''

def timestamp_transfer(timestamp):
    '''
    Translate timestamp into readeable time.
    '''
    if timestamp // 1000000000000:
        dt = datetime.datetime.fromtimestamp(timestamp/1000)
    else:
        dt = datetime.datetime.fromtimestamp(timestamp)
    return("时间戳 {} 对应的时间是：{}".format(timestamp, dt))

def server_time(client_obj):
    '''
    Return current time from the sever(spot or future)
    '''
    return client_obj.time()['serverTime']

def spot_latest_hold(spot_snapshot, asset_name):
    if type(spot_snapshot) == dict:
        current_hold = pd.DataFrame(spot_snapshot['snapshotVos'][-1]['data']['balances'])
    else:
        current_hold = pd.DataFrame(spot_snapshot)
    # current_timestamp = spot_snapshot['snapshotVos'][-1]['updateTime']
    asset_hold = current_hold[current_hold['asset'] == asset_name]
    # asset_hold['timestamp'] = pd.Series([current_timestamp]*len(asset_hold))
    return asset_hold

def future_pickup(c_future_balance, asset):
    targetasset = c_future_balance[c_future_balance['asset']==asset]
    future_net_value = float(targetasset['balance'].values[0]) + float(targetasset['crossUnPnl'].values[0])
    future_timestamp = targetasset['updateTime'].values[0]
    return future_net_value, future_timestamp

def get_the_total_value():
    snapshot = spot_client.account_snapshot(type='SPOT',limit = 30)
    spot_held = spot_latest_hold(snapshot,'BETH')
    spot_held['ticker_price'] = spot_client.ticker_price(symbol='BETHUSDT')['price']
    spot_net_value = float(spot_held['free'][0])*float(spot_held['ticker_price'][0])

    c_future_balance = pd.DataFrame(future_client.balance())
    future_net_value, future_timestamp = future_pickup(c_future_balance, 'USDT')
    total_value = future_net_value + spot_net_value
    return total_value, future_timestamp

def get_the_total_value_v2():
    snapshot = spot_client.user_asset()
    spot_held = spot_latest_hold(snapshot,'BETH')
    spot_held['ticker_price'] = spot_client.ticker_price(symbol='BETHUSDT')['price']
    spot_net_value = float(spot_held['free'][0])*float(spot_held['ticker_price'][0])

    c_future_balance = pd.DataFrame(future_client.balance())
    future_net_value, future_update_timestamp = future_pickup(c_future_balance, 'USDT')
    total_value = future_net_value + spot_net_value
    return total_value

if __name__ == '__main__':
    total_value = get_the_total_value_v2()
    current_timestamp = server_time(spot_client)
    #Construct the data needed to be insert
    new_data = {'timestamp':current_timestamp, 'total_netvalue':total_value}


    logfile = pd.read_csv( config.get('local_setting', 'nv_log') )
    logfile.loc[len(logfile)] = new_data
    logfile.to_csv(config.get('local_setting', 'nv_log'), index=False)