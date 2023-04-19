import requests
import urllib.request
import zipfile
import io

url = 'https://data.binance.vision/'
BETHroute = '?prefix=data/spot/daily/trades/BETHUSDT/'
ETHContraceRoute = '?prefix=data/futures/cm/daily/trades/ETHUSD_PERP/'

zipfileurl = 'https://data.binance.vision/data/spot/daily/klines/BETHUSDT/1d/BETHUSDT-1d-2023-04-17.zip'

def get_close(link):
    with urllib.request.urlopen(link) as response:
        zip_data = response.read()

    with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
        for name in zip_file.namelist():
            with zip_file.open(name) as file:
                content = file.read()
    
    content = str(content).strip("b'\\n'")
    print(content)
    arr = [x.strip() for x in s.split(",")]
    arr = [int(arr[0])] + [float(x) for x in arr[1:]]
    
    return content

if __name__ == '__main__':
    content = get_close(zipfileurl)
    pass