import requests
import json
import pickle
import pandas as pd
import os

data = pd.read_csv('analysis.csv')
ip = data['ip']
root = os.getcwd() + '\\ip_cache'
key = '18ef9803c3e0b38af8a7f6649d1d17b9'
if not os.path.exists(root):
    all_data = {'start': 0}
    index = all_data.get('start')
else:
    with open('ip_cache', 'rb') as f:
        all_data = pickle.load(f)
    index = all_data.get('start')
for i in ip[index:]:
    check = all_data.get(i)
    if check:
        index += 1
        continue
    params = {'key': key, 'ip': i}
    try:
        data = requests.get('https://restapi.amap.com/v3/ip?', params=params)
        if data.status_code == 200:
            data = data.content
            data = json.loads(data)
            if data['province'] == data['city']:
                all_data[i] = data['province']
            else:
                all_data[i] = data['province'] + data['city']
            index += 1
        else:
            break
    except:
        break
all_data['start'] = index
local = list(all_data.values())
for i in local:
    if type(i) != int:
        print(i)
        params = {'key': key, 'address': i}
        try:
            data = requests.get('https://restapi.amap.com/v3/geocode/geo?', params=params)
            if data.status_code == 200:
                data = data.content
                data = json.loads(data)
                all_data[i] = data['geocodes'][0]['location']
            else:
                break
        except:
            break
    else:
        continue
with open('ip_cache', 'wb') as f:
    pickle.dump(all_data, f)
with open('ip_cache', 'rb') as f:
    print('最新数据：', pickle.load(f))
