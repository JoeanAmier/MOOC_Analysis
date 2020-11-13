from flask import Flask
import pickle
from flask import render_template
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def index():
    with open('data', 'rb') as f:
        data = pickle.load(f)
    unvalid = data[0] - data[1]
    valid = data[1]
    title = data[2]
    mark = {}
    for i, j in enumerate(title.values()):
        mark[j] = '课程' + str(i + 1)
    local = dict(data[3])
    local_1 = list(local.keys())
    local_2 = list(local.values())
    click = data[4]
    click = sorted(click.items(), key=lambda x: x[1], reverse=True)
    for i, j in enumerate(click):
        click[i] = list(j)
        click[i].append(mark[title[j[0]]])
        click[i].append(title[j[0]])
    data = add_data()[:1000]
    return render_template('index.html', local_1=local_1, local_2=local_2, unvalid=unvalid, valid=valid,
                           click=click, data=data)


@app.route('/source/')
def source():
    data = pd.read_csv('analysis.csv')
    data = np.array(data[:5000])
    data = data.tolist()
    return render_template('source.html', data=data)


@app.route('/data/')
def data():
    data = add_data()
    data = np.array(data[:5000])
    data = data.tolist()
    return render_template('data.html', data=data)


def add_data():
    data = pd.read_csv('analysis.csv')
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
    return np.array(data).tolist()


@app.route('/group/')
def group():
    with open('group', 'rb') as f:
        data = []
        cache = pickle.load(f)
        for i in cache:
            item = []
            item.append(i[0])
            num = 0
            item.append(i[1])
            for j in i[2]:
                num += j[2]
            item.append(num)
            data.append(item)
    return render_template('group.html', data=data)


@app.route('/groups/')
def groups():
    with open('group', 'rb') as f:
        data = pickle.load(f)
    return render_template('groups.html', data=data)


if __name__ == '__main__':
    app.run()
