---
title: juc-ScheduledFutureTask和ScheduledExecutorService-ScheduledThreadPoolEx.md
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
title: juc-ScheduledFutureTask和ScheduledExecutorService-ScheduledThreadPoolEx.md
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
ScheduledFutureTask
ScheduledExecutorService 接口


ScheduledThreadPoolExecutor 实现类
~~~
    public static void main(String[] args) {
        ScheduledThreadPoolExecutor executor = new ScheduledThreadPoolExecutor(10,
            new Builder().namingPattern("schedule-pool-%d").daemon(true).build()) {
            @Override
            protected void afterExecute(Runnable r, Throwable t) {
                super.afterExecute(r, t);
                Threads.printException(r, t);
            }
        };

        TimerTask timerTask = new TimerTask() {
            @Override
            public void run() {
                System.out.println("ThreadPoolConfig.run");
            }
        };
        executor.scheduleAtFixedRate(timerTask,1,1,TimeUnit.SECONDS);
        try {
            Thread.sleep(10000000000000000L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }
~~~
