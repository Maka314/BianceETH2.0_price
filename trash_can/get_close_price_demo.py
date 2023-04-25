import urllib.request
import zipfile
import io
import pandas as pd
import time

fileName = 'SpotKlineData.csv'


def get_close(link):
    with urllib.request.urlopen(link) as response:
        zip_data = response.read()

    with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
        for name in zip_file.namelist():
            with zip_file.open(name) as file:
                content = file.read()
    
    content = str(content).strip("b'\\n'")
    arr = [x.strip() for x in content.split(",")]
    arr = [int(arr[0])] + [float(x) for x in arr[1:]]
    
    return arr

if __name__ == '__main__':
    # 获取当前时间戳
    timestamp = time.time()-1*24*60*60
    date = time.strftime('%Y-%m-%d', time.gmtime(timestamp))
    zipfileurl = 'https://data.binance.vision/data/spot/daily/klines/BETHUSDT/1d/BETHUSDT-1d-%s.zip'%(date) #be like this '2023-04-19'
    content = get_close(zipfileurl)
    
    csv_file = pd.read_csv(fileName)
    dictContent = {k: v for k, v in zip(list(csv_file.columns), content)}
    csv_file = pd.concat([csv_file, pd.DataFrame(dictContent,index=[0])]).drop_duplicates(subset=['Opentime'])
    csv_file.to_csv(fileName,index=False)