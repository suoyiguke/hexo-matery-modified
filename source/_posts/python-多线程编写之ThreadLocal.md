---
title: python-多线程编写之ThreadLocal.md
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
title: python-多线程编写之ThreadLocal.md
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
python 线程库实现了 ThreadLocal 变量 (Java 语言有类似的实现)。ThreadLocal 真正做到了线程之间的数据隔离，并且使用时不需要手动获取自己的线程 ID。

###使用案例
~~~

import threading

global_data = threading.local()


def thread_cal():
    global_data.num = 0
    for _ in range(1000):
        global_data.num += 1
    print(threading.current_thread().getName(), global_data.num)


threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

for i in range(10):
    threads[i].join()

print("Main thread: ", global_data)
~~~

每个线程都可以通过 global_data.num 获得自己独有的数据，并且每个线程读取到的 global_data 都不同，真正做到线程之间的隔离。
Python 的 WSGI 工具库 werkzeug 中有一个更好的 ThreadLocal 实现，甚至支持协程之间的私有数据，实现更加复杂。



- 在脚本中经常会遇到需要线程之间隔离的变量， 尝试用过全局变量，但是为了线程安全要加锁从而影响执行效率
- 也用过函数的参数传递，太麻烦

###怎么获取所有local的所有线程隔离实例？
用作回收复用的资源
