---
title: juc---线程池之四种拒绝策略.md
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
title: juc---线程池之四种拒绝策略.md
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
###为什么要使用拒绝策略？
等待队列已经排满了，再也塞不下新任务了
同时，线程池中的max线程也达到了，无法继续为新任务服务。
 
这个是时候我们就需要拒绝策略机制合理的处理这个问题。

###四种拒绝策略介绍

jdk中自带的拒绝策略均实现了java.util.concurrent.RejectedExecutionHandler接口

######AbortPolicy
默认的拒绝策略。直接抛出 java.util.concurrent.RejectedExecutionException异常
~~~
 new ThreadPoolExecutor.AbortPolicy()
~~~
~~~
import java.util.concurrent.*;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());
        try {
            for (int i = 1; i <= 9; i++) {
                executorService.execute(new Runnable() {
                    @Override
                    public void run() {
                        System.out.println(Thread.currentThread().getName() + " 办理业务");
                    }
                });
            }
        } finally {
            executorService.shutdown();
        }

    }
}
~~~
######CallerRunsPolicy
将任务返还给调用者线程执行
~~~
new ThreadPoolExecutor.CallerRunsPolicy()
~~~

~~~
import java.util.concurrent.*;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.CallerRunsPolicy());
        try {
            for (int i = 1; i <= 9; i++) {
                executorService.execute(new Runnable() {
                    @Override
                    public void run() {
                        System.out.println(Thread.currentThread().getName() + " 办理业务");
                    }
                });
            }
        } finally {
            executorService.shutdown();
        }

    }
}
~~~
执行结果： 任务果然返还给main线程了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d4b23351b96a1461.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######DiscardPolicy
直接抛弃无法处理的任务，不予处理不抛异常。如果业务汇总允许任务丢失，这是最好的策略
~~~
new ThreadPoolExecutor.DiscardPolicy()
~~~
查看执行结果，只有8个。第9个被抛弃
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d1eea0ef6b2b67d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######DiscardOldestPolicy
抛弃队列中等待最久的任务，然后把当前任务加入队列中尝试再次提交当前任务
~~~
new ThreadPoolExecutor.DiscardOldestPolicy()
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-4df9636792b0d54a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
