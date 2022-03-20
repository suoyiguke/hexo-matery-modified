---
title: Condition的awaitNanos和await区别.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: Condition的awaitNanos和await区别.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
 long awaitNanos(long nanosTimeout) throws InterruptedException;


void await() throws InterruptedException;
boolean await(long time, TimeUnit unit) throws InterruptedException;


    //等待指定时间，此时不唤醒，则会在5秒后唤醒
//            condition.await(5,TimeUnit.SECONDS);

            //返回值表示剩余时间，如果在nanosTimesout之前唤醒，那么返回值 = nanosTimeout - 消耗时间，
            // 如果返回值 <= 0 ,则可以认定它已经超时了。
            long nanos = TimeUnit.SECONDS.toNanos(5);
            long x = condition.awaitNanos(nanos);
            System.out.println(x);
/114082363
