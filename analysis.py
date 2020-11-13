import pandas as pd
import requests
import re
import html
import pickle
import numpy as np


def read_data():
    data = pd.read_csv('analysis.csv')
    return data


def analyze_data(all, valid, data):
    find = re.compile(r'<title>(.*?)</title>', re.DOTALL)
    link_counts = data['link'].value_counts()
    title_dict = {}
    for i in link_counts.keys():
        title = requests.get(i)
        title = title.content.decode(title.encoding)
        title = re.findall(find, title)[0]
        title = title.replace('\n', '')
        title = html.unescape(title)
        if title == '慕课网':
            title_dict[i] = '该门课程已经下架'
        else:
            title_dict[i] = title
    groups = []
    link_local = data.groupby(['link', 'local'])
    for (k1, k2), group in link_local:
        cache = []
        cache.append(title_dict[k1])
        cache.append((k1, k2))
        group = np.array(group)
        group = group.tolist()
        cache.append(group)
        groups.append(cache)
    with open('group', 'wb') as f:
        pickle.dump(groups, f)
    local_counts = data['local'].value_counts()
    clicked_counts = {}
    link_group = data.groupby('link')
    for i, j in link_group:
        clicked_counts[i] = j['num'].sum(axis=0)
    sorted(clicked_counts.items(), key=lambda x: x[1], reverse=True)
    data['time'] = data['time'].astype('str')
    time_index = pd.date_range(start='2017-05-11 00:00:00', periods=24, freq='H')
    time_counts = {}
    for i in range(len(time_index) - 1):
        time_count = data[(str(time_index[i]) <= data['time']) & (data['time'] < str(time_index[i + 1]))]
        time_counts[str(time_index[i]) + '-' + str(time_index[i + 1])] = len(time_count)
    data = [all, valid, title_dict, local_counts, clicked_counts, time_counts]
    return data


def add_data(data):
    with open('ip_cache', 'rb') as f:
        locals = []
        file = pickle.load(f)
        for i in data['ip']:
            local = file.get(i)
            if local is None:
                break
            else:
                locals.append(local)
    if len(locals) == len(data['ip']):
        data['local'] = locals
    else:
        raise ValueError
    Coordinates = []
    for i in data['local']:
        cache = file.get(i)
        Coordinates.append(cache)
    if len(locals) == len(data['ip']):
        data['Coordinates'] = Coordinates
    else:
        raise ValueError
    return data


def save_data(data):
    with open('data', 'wb') as f:
        pickle.dump(data, f)


def main():
    data_0 = read_data()
    data = data_0.drop(
        data_0[(data_0['link'] == 'http://www.imooc.com/video/4600') | (
                data_0['link'] == 'http://www.imooc.com/video/4500')].index)
    all = len(data_0)
    valid = len(data)
    data = add_data(data)
    data = analyze_data(all, valid, data)
    save_data(data)


if __name__ == '__main__':
    main()
