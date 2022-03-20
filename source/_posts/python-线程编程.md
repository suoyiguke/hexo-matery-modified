---
title: python-线程编程.md
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
title: python-线程编程.md
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

###创建一个线程试试

~~~
import threading
from threading import Thread
def sendx(str):
    print(str)
    t = threading.currentThread()
    print(t.getName())
    print(t.isAlive())
    print(t.is_alive())
    print(t.isDaemon())

    list = threading.enumerate()
    for tz in list:
        print(tz.getName())

    print(threading.activeCount())
    print(len(threading.enumerate()))


# 用线程去执行函数
t = Thread(target=sendx, args=('sss',))
t.start()
t.setName("线程A")




~~~
1、执行线程
t.start()

2、返回当前线程实例
 t = threading.currentThread()

3、获得线程名
print(t.getName())

4、判断线程是否活动
print(t.isAlive())

5、判断是否为守护线程
 print(t.isDaemon())

6、返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
threading.enumerate(): 

7、返回正在运行的线程数量
threading.activeCount()和len(threading.enumerate())都行

###线程join

 join()阻塞当前上下文环境的线程， 当前线程等待指定线程终止

使用join实现MainThread线程等待所有子线程
~~~
import threading
import time
from concurrent.futures import thread
from threading import Thread

def threadSend(url):
    time.sleep(3)
    print('线程名==>'+threading.currentThread().getName()+'url==>'+url)

def mian_sj():
    # 线程list
    threads = []
    url_list = []

    # 英雄联盟  王者荣耀 APEX  刺激战场 我的世界
    url_list.append('http://v.huya.com/g/vhuyalol?set_id=4&order=new&page=')
    url_list.append('http://v.huya.com/g/vhuyajdqs?set_id=4&order=new&page=')
    url_list.append('http://v.huya.com/g/vhuyawzry?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/apex?set_id=6&order=new&page=')
    url_list.append('http://v.huya.com/g/cjzc?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/vhuyamc?set_id=6&order=new&page=')

    # 其他的 第五人格 荒野行动 CF手游 全军出击 QQ飞车手游 火影忍者手游
    url_list.append('http://v.huya.com/g/id5?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/vhuyahyxd?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/cfm?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/qjcj?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/vhuyaqqfcsy?set_id=3&order=new&page=')
    url_list.append('http://v.huya.com/g/vhuyahyrz?set_id=3&order=new&page=')

    for url in url_list:
        p = Thread(target=threadSend, args=(url,))
        p.start()
        threads.append(p)

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("虎牙--退出主线程")

if __name__ == '__main__':
    mian_sj()
~~~

###sleep
~~~
import time
time.sleep(3)
~~~
