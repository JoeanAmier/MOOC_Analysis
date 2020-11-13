import pickle
import numpy as np
import pandas as pd

with open('data', 'rb') as f:
    # print(pickle.load(f))
    data = pickle.load(f)[-1]
    for i in data.keys():
        print(i[-8:-3], data[i])
# with open('group', 'rb') as f:
#     data = pickle.load(f)
#     print(data[0][0])

# data = np.array([[1, 2], [3, 4], [5, 6]])
# data = pd.DataFrame(data)
# data = data.drop(data[data[0] < 3])
# print(data)
