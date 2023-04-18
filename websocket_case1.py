import websocket
import json
import hmac
import hashlib
import time

# 币安API Key和Secret Key
api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_SECRET_KEY'

# Websocket服务端URL和订阅主题
url = 'wss://stream.binance.com:9443/ws/btcusdt@trade'
topic = 'btcusdt@trade'

# 生成签名
timestamp = int(time.time() * 1000)
signature = hmac.new(secret_key.encode(), f'timestamp={timestamp}'.encode(), hashlib.sha256).hexdigest()

# 订阅消息
sub_message = {
    'method': 'SUBSCRIBE',
    'params': [topic],
    'id': 1,
    'key': api_key,
    'signature': signature,
    'timeStamp': timestamp
}

# Websocket连接回调函数
def on_open(ws):
    ws.send(json.dumps(sub_message))

# Websocket接收数据回调函数
def on_message(ws, message):
    print(message)

# Websocket错误回调函数
def on_error(ws, error):
    print(error)

# Websocket关闭回调函数
def on_close(ws):
    print("Websocket连接已关闭")

# 建立Websocket连接
ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
ws.run_forever()
