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


def timestamp_transfer(timestamp):
    '''
    Translate timestamp into readeable time.
    '''
    if timestamp // 1000000000000:
        dt = datetime.datetime.fromtimestamp(timestamp/1000)
    else:
        dt = datetime.datetime.fromtimestamp(timestamp)
    return("时间戳 {} 对应的时间是：{}".format(timestamp, dt))

def server_time(client):
    '''
    Return current time from the sever(spot or future)
    '''
    return client.time()['serverTime']

def spot_latest_hold(client, asset:str):
    '''
    Func to access current spot hold.
    '''
    current = pd.DataFrame(client.account()['balances'])
    target_asset_hold = current[current['asset']==asset]
    return float(target_asset_hold['free'].values[0])

def share_history(client, asset:str, limit=20):
    sharedata = client.asset_dividend_record(asset = asset, limit = limit)['rows']
    pd_sharedata = pd.DataFrame(sharedata)
    return(pd_sharedata)

def share_history_selection(client, asset:str, p_time, q_time):
    share_data = share_history(client, asset)
    get_limit = 20
    while min(share_data['divTime']) > p_time:
        get_limit += 10
        share_data = share_history(client, asset, limit=get_limit)
    cutted_data = share_data[(share_data['divTime']>p_time) & (share_data['divTime']<q_time)]
    return cutted_data
    
def get_fa_balance_pal(client, asset:str = 'USDT'):
    fa_asset = pd.DataFrame(client.balance())
    asset = fa_asset[fa_asset['asset']==asset]
    fa_balance, fa_pal = asset['balance'].values[0], asset['crossUnPnl'].values[0]
    fa_balance, fa_pal = float(fa_balance), float(fa_pal)
    return (fa_balance, fa_pal)

def get_fa_funding_fee(client, limit=100):
    data = client.get_income_history(incomeType = 'FUNDING_FEE',limit = limit)
    pd_data = pd.DataFrame(data)
    return pd_data

def get_fa_funding_fee_selection(client, p_time, q_time):
    fee_history = get_fa_funding_fee(client)
    get_limit = 100
    while min(fee_history['time']) > p_time:
        get_limit += 50
        fee_history = get_fa_funding_fee(client, limit= get_limit)
    cutted_data = fee_history[(fee_history['time']>p_time) & (fee_history['time']<q_time)]
    return cutted_data

if __name__ == '__main__':
    logfile = pd.read_csv( config.get('local_setting', 'nv_log') )
    current_timestamp, latest_timestamp =server_time(spot_client), max(logfile['timestamp'])
    spot_price = float(spot_client.ticker_price(symbol='BETHUSDT')['price'])
    spot_current_hold = spot_latest_hold(spot_client, 'BETH')
    spot_share_history = share_history_selection(spot_client, 'BETH', latest_timestamp, current_timestamp)
    spot_share_sumup = sum(spot_share_history['amount'].astype(float))
    fa_balance, fa_pal = get_fa_balance_pal(future_client)
    fa_fee_history = get_fa_funding_fee_selection(future_client,latest_timestamp, current_timestamp)
    fa_fee_sumup = sum(fa_fee_history['income'].astype(float))
    total_netvalue = sum([spot_current_hold*spot_price, fa_balance, fa_pal])

    new_data = [current_timestamp,total_netvalue,spot_current_hold,spot_share_sumup,spot_price,fa_balance, fa_pal,fa_fee_sumup]

    logfile.loc[len(logfile)] = new_data
    logfile.to_csv(config.get('local_setting', 'nv_log'), index=False)