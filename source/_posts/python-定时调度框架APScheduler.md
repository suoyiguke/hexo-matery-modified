---
title: python-定时调度框架APScheduler.md
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
title: python-定时调度框架APScheduler.md
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
APScheduler基于Quartz的一个Python定时任务框架，实现了Quartz的所有功能，使用起来十分方便。提供了基于日期、固定时间间隔以及crontab类型的任务，并且可以持久化任务。基于这些功能，我们可以很方便的实现一个python定时任务系统。


######安装
~~~
pip install apscheduler
~~~

######每隔5s执行一次
~~~
import time
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()



def my_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(my_job, 'interval', seconds=5)
    sched.start()

~~~

######每天定时执行
~~~
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

def job2():
    print('job2执行')

if __name__ == "__main__":
    sched = BlockingScheduler()
    # 表示每天15:10（PM)直到2020-05-30执行一次job2函数
    sched.add_job(job2, 'cron', day_of_week='0-6', hour=15, minute=10, end_date='2020-05-30')
    sched.start()
~~~
######按星期英文简写执行

日期简写英文
~~~
date 日期
mon 星期一
tue 星期二
wed 星期三
thu 星期四
fri 星期五
sat 星期六
sun 星期日
~~~
~~~
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

def job2():
    print('job2执行')

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(job2, 'cron', day_of_week='mon,tue,wed,thu,fri,sat,sun', hour=15, minute=12, end_date='2020-05-30')
    sched.start()
~~~
######指定时间，执行一次
~~~
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

def job2():
    print('job2执行')

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(job2, 'date', run_date='2020-02-15 15:13:50')
    sched.start()
~~~

######马上执行且隔4秒执行一次
~~~
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

def job2():
    print('job2执行')

if __name__ == "__main__":
    sched = BlockingScheduler()
    sched.add_job(job2, 'interval', seconds=4, next_run_time=datetime.datetime.now())
    sched.start()
~~~
