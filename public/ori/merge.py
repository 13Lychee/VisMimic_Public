# 合并每个json文件的对象到一个数组中

import json
import os

path = './zhengshitu/'

with open('merge.json', 'w') as f:
    f.write('[')
    for i in range(1, 168):
        with open(path + str(i).zfill(4) + '_keypoints.json', 'r') as f1:
            data = json.load(f1)
            if i != 1:
                f.write(',')
            f.write(json.dumps(data))
    f.write(']')
    