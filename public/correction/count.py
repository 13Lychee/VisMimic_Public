# 统计每个文件夹里的最大标号图片
import json
import os

with open('frames.json', 'w') as f:
    f.writelines('[')
    for dir1 in os.listdir('.'):
        if not os.path.isdir(dir1):
            continue
        f.write('[')
        for dir2 in os.listdir(dir1):
            if not os.path.isdir(dir1 + '/' + dir2):
                continue
            number = 0
            for file in os.listdir(dir1 + '/' + dir2):
                if file.endswith('.png') and file.split('.')[0].isdigit():
                    number = max(number, int(file.split('.')[0]))
            f.write(str(number) + ',')
        f.writelines('],')
    f.writelines(']')

# 去掉多余的逗号
with open('frames.json', 'r') as f:
    data = f.read()
    data = data.replace(',]', ']')
    
with open('frames.json', 'w') as f:
    f.write(data)
