from binance.spot import Spot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key, api_secret = config.get('biance_api', 'api_key'), config.get('biance_api', 'secret')

client = Spot(api_key=api_key, api_secret=api_secret)
print(client.account())