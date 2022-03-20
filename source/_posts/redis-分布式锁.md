---
title: redis-分布式锁.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis-分布式锁.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
###redis分布式锁实现

SET KEY VALUE [EX seconds] [PX milliseconds] [NX|XX]

>1、VALUE  - 设置锁的名字
2、EX seconds − 设置指定的到期时间(以秒为单位)。
3、PX milliseconds - 设置指定的到期时间(以毫秒为单位)。
4、NX - 仅在键不存在时设置键。
5、XX - 只有在键已存在时才设置。

实现互斥锁需要用到以上命令，比如：
~~~
//设置“锁”
if(redis.set("lock", "1", "EX 180", "NX")){
    //业务逻辑
    .......
    //执行完业务逻辑后，释放锁
    redis.delete("lock");
}
~~~

因为“NX”保证了只有redis没有该键才会设值该键值对，这样只有第一次访问的线程才能执行后面的逻辑，后面的线程再访问，只能阻塞等待




###RedisLockRegistry 工具
