---
title: redission.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 分布式锁
categories: 分布式锁
---
---
title: redission.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 分布式锁
categories: 分布式锁
---
这种写法一线互连网公司已经实现好多年了！放心使用！
~~~
RLock redissionLock =  redission.getLock(lockKey);
trt{
redissionLock .lock(30,TimeUnit.SECONDS);

}finally{
redissionLock.unlock();
}
~~~
