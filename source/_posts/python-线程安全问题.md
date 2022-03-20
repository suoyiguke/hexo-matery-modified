---
title: python-线程安全问题.md
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
title: python-线程安全问题.md
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
###两个线程并发累加一个全局变量

理论上，最终得到的数据应该是2000000，而运行结果是少于这个值的
~~~
import threading
import time
from threading import Thread
global_num = 0

def func1():
    global global_num
    for i in range(1000000):
        global_num += 1
    print(threading.currentThread().getName()+'==>'+str(global_num))


def func2():
    global global_num
    for i in range(1000000):
        global_num += 1
    print(threading.currentThread().getName() + '==>' + str(global_num))




t1 = Thread(target=func1)
t1.start()
t2 = Thread(target=func2)
t2.start()
time.sleep(5)

print(global_num)


~~~

###使用添加互斥锁手段，解决并发安全问题

lock = Lock()

lock.acquire()
        。。。。。
lock.release()

执行结果为2000000

~~~
import threading
import time
from threading import Thread,Lock

lock = Lock()
global_num = 0

def func1():
    global global_num
    for i in range(1000000):
        lock.acquire()
        global_num += 1
        lock.release()
    print(threading.currentThread().getName()+'==>'+str(global_num))


def func2():
    global global_num
    for i in range(1000000):
        lock.acquire()
        global_num += 1
        lock.release()
    print(threading.currentThread().getName() + '==>' + str(global_num))




t1 = Thread(target=func1)
t1.start()
t2 = Thread(target=func2)
t2.start()
time.sleep(5)

print(global_num)

~~~
