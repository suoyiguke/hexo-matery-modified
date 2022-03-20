---
title: python-文件操作笔记.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: python-文件操作笔记.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
######文件夹不存在则创建文件
~~~
home = 'E:\\gggg\\zzzzz'
print(home)  # Print the location
if not os.path.exists(home):  # os.path.join() for making a full path safely
    os.makedirs(home)  # If not create the directory, inside their home directory
else:
    print(print('存在'))
~~~
######读取yml文件
~~~
import yaml


def get_config():
    with open('./test_config.yml', 'r', encoding="utf-8") as f:
        data = yaml.load(f.read(), Loader=yaml.FullLoader)
    return data


# 打印测试
if __name__ == '__main__':
    print(get_config())

~~~ 

######读取文件的一行
~~~
f = open('E:/py/redis/src/testz.py',encoding='UTF-8')  # 打开文件
list = f.readlines()
for line in list:
    print(line)
~~~

######下载网络图片到本地
~~~
import urllib.request
urllib.request.urlretrieve('https://upload.jianshu.io/users/upload_avatars/13965490/0b5afc86-d568-469a-9fb2-ff80665d293f?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96/format/webp','./1.png');
~~~

######文件路径拼接
~~~
import os

TESTDIR = 'testdir'
home = 'E:\\gggg\\zzzz'
join = os.path.join(home, TESTDIR)
print(join)
~~~

######读取文件夹下所有文件
~~~
import os
fileList = os.listdir("D:\搜狗高速下载\data\excel")
print(fileList)
~~~

######文件改名
~~~
import os

# 按行读取
f = open('D:\\搜狗高速下载\\data\\name.txt',encoding='UTF-8')  # 打开文件
list = f.readlines()
for line in list:
    print(line.strip('\n'))


path = "D:\\搜狗高速下载\\data\\excel\\"
fileList = os.listdir(path)
i = 0
for file in fileList:
    # print(file[0:-4])
    # oldName = file[0:-4]
    strip = list[i].strip('\n')
    os.rename(path+file, path + strip+'.xls')
    i=i+1;

~~~
