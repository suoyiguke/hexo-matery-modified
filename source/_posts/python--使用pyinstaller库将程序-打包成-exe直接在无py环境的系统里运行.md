---
title: python--使用pyinstaller库将程序-打包成-exe直接在无py环境的系统里运行.md
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
title: python--使用pyinstaller库将程序-打包成-exe直接在无py环境的系统里运行.md
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
###安装依赖
命令安装
~~~
pip install pyinstaller
~~~

网络不行，就离线安装
http://www.pyinstaller.org/downloads.html



###简单使用，将 py文件打包成exe
~~~
pyinstaller test1.py
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-14042ec912a13811.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样生成的exe就可以直接执行了

###打包成单个exe
~~~
pyinstaller -F test.py
~~~

###运行报找不到依赖解决

这里我已pychar举例子，按安装的python位置填后面一段，连着包一起打包，这样程序能运行打包就能成功了
~~~
pyinstaller test.py -F -p C:\Users\yinkai\AppData\Local\Programs\Python\Python38\Lib\site-packages
~~~


###我的解决方式

~~~
F:\py\windowsrun>F:\py\windowsrun\dist\test.exe
Traceback (most recent call last):
  File "test.py", line 7, in <module>
    _instance = create_engine(
  File "sqlalchemy\engine\__init__.py", line 488, in create_engine
  File "sqlalchemy\engine\strategies.py", line 87, in create
  File "sqlalchemy\dialects\mysql\pymysql.py", line 62, in dbapi
ModuleNotFoundError: No module named 'pymysql'
[4428] Failed to execute script test
~~~

直接忽略这个pymysql依赖
~~~
pyinstaller test.py -F  --hidden-import pymysql
~~~

###各种打包出错
1、python3.8 + matplotlib 3.3.2  会报错 
>:\Users\yinkai\AppData\Local\Programs\Python\Python38\lib\site-packages\pyinstaller-4.0-py3.8.egg\PyInstaller\loader\pyimod0
_importers.py:493: MatplotlibDeprecationWarning: Matplotlib installs where the data is not in the mpl-data subdirectory of t
e package are deprecated since 3.2 and support for them will be removed two minor releases later.

解决使用 python3.7.7 + matplotlib 3.1.1 



###打包指定依赖另一种办法
就是直接把文件放到site-packages下打包！
