---
title: DelayQueue-延时队列.md
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
title: DelayQueue-延时队列.md
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
###一、DelayQueue是什么
　　DelayQueue是一个无界的BlockingQueue，用于放置实现了Delayed接口的对象，其中的对象只能在其到期时才能从队列中取走。这种队列是有序的，即队头对象的延迟到期时间最长。注意：不能将null元素放置到这种队列中。

###二、DelayQueue能做什么
　1. 淘宝订单业务:下单之后如果三十分钟之内没有付款就自动取消订单。 
　2. 饿了吗订餐通知:下单成功后60s之后给用户发送短信通知。

　3.关闭空闲连接。服务器中，有很多客户端的连接，空闲一段时间之后需要关闭之。

　4.缓存。缓存中的对象，超过了空闲时间，需要从缓存中移出。

　5.任务超时处理。在网络协议滑动窗口请求应答式交互时，处理超时未响应的请求等。




###三、怎么办，具体代码
- DelayQueue只能添加(offer/put/add)实现了Delayed接口的对象，意思是说我们不能想往DelayQueue里添加什么就添加什么，不能添加int、也不能添加String进去，必须添加我们自己的实现了Delayed接口的类的对象。
-  元素进入队列后，先进行排序，然后，只有getDelay也就是剩余时间为0的时候，该元素才有资格被消费者从队列中取出来，所以构造函数一般都有一个时间传入。




~~~
package com.company;

import java.util.concurrent.DelayQueue;
import java.util.concurrent.Delayed;
import java.util.concurrent.TimeUnit;

public class MyDelayedTask implements Delayed {
    private String name;
    private long start = System.currentTimeMillis();
    private long time;

    public MyDelayedTask(String name, long time) {
        this.name = name;
        this.time = time;
    }

    /**
     * 需要实现的接口，获得延迟时间   用过期时间-当前时间
     *
     * @param unit
     * @return
     */
    @Override
    public long getDelay(TimeUnit unit) {
        return unit.convert((start + time) - System.currentTimeMillis(), TimeUnit.MILLISECONDS);
    }

    /**
     * 用于延迟队列内部比较排序   当前时间的延迟时间 - 比较对象的延迟时间
     *
     * @param o
     * @return
     */
    @Override
    public int compareTo(Delayed o) {
        return (int) (this.getDelay(TimeUnit.MILLISECONDS) - o.getDelay(TimeUnit.MILLISECONDS));
    }

    @Override
    public String toString() {
        return "MyDelayedTask{" +
                "name='" + name + '\'' +
                ", time=" + time +
                '}';
    }


    private static DelayQueue delayQueue  = new DelayQueue();
    public static void main(String[] args) throws InterruptedException {

        new Thread(new Runnable() {
            @Override
            public void run() {
                delayQueue.offer(new MyDelayedTask("task1",10000));
                delayQueue.offer(new MyDelayedTask("task2",3900));
                delayQueue.offer(new MyDelayedTask("task3",1900));
                delayQueue.offer(new MyDelayedTask("task4",5900));
                delayQueue.offer(new MyDelayedTask("task5",6900));
                delayQueue.offer(new MyDelayedTask("task6",7900));
                delayQueue.offer(new MyDelayedTask("task7",4900));
            }
        }).start();

        while (true) {
            Delayed take = delayQueue.take();
            System.out.println(take);
        }
    }
}

~~~


###四、原理


*   可重入锁
*   用于根据delay时间排序的优先级队列
*   用于优化阻塞通知的线程元素leader
*   用于实现阻塞和通知的Condition对象

### delayed和PriorityQueue

　在理解delayQueue原理之前我们需要先了解两个东西,delayed和PriorityQueue.

*   delayed是一个具有过期时间的元素
*   PriorityQueue是一个根据队列里元素某些属性排列先后的顺序队列

　　delayQueue其实就是在每次往优先级队列中添加元素，然后以元素的delay/过期值作为排序的因素，以此来达到先过期的元素会拍在队首,每次从队列里取出来都是最先要过期的元素

### offer方法

1.  执行加锁操作
2.  吧元素添加到优先级队列中
3.  查看元素是否为队首
4.  如果是队首的话，设置leader为空，唤醒所有等待的队列
5.  释放锁

代码如下：

~~~
<pre style="margin: 0px; padding: 0px; transition-duration: 0.2s; transition-property: color, opacity; overflow: auto; font-family: inherit !important; font-size: 12px; overflow-wrap: break-word; color: rgb(101, 108, 115);">public boolean offer(E e) { final ReentrantLock lock = this.lock;
        lock.lock(); try {
            q.offer(e); if (q.peek() == e) {
                leader = null;
                available.signal();
            } return true;
        } finally {
            lock.unlock();
        }
    }
~~~

### take方法

1.  执行加锁操作
2.  取出优先级队列元素q的队首
3.  如果元素q的队首/队列为空,阻塞请求
4.  如果元素q的队首(first)不为空,获得这个元素的delay时间值
5.  如果first的延迟delay时间值为0的话,说明该元素已经到了可以使用的时间,调用poll方法弹出该元素,跳出方法
6.  如果first的延迟delay时间值不为0的话,释放元素first的引用,避免内存泄露
7.  判断leader元素是否为空,不为空的话阻塞当前线程
8.  如果leader元素为空的话,把当前线程赋值给leader元素,然后阻塞delay的时间,即等待队首到达可以出队的时间,在finally块中释放leader元素的引用
9.  循环执行从1~8的步骤
10.  如果leader为空并且优先级队列不为空的情况下(判断还有没有其他后续节点),调用signal通知其他的线程
11.  执行解锁操作

~~~
<pre style="margin: 0px; padding: 0px; transition-duration: 0.2s; transition-property: color, opacity; overflow: auto; font-family: inherit !important; font-size: 12px; overflow-wrap: break-word; color: rgb(101, 108, 115);">public E take() throws InterruptedException { final ReentrantLock lock = this.lock;
        lock.lockInterruptibly(); try { for (;;) {
                E first = q.peek(); if (first == null)
                    available.await(); else { long delay = first.getDelay(NANOSECONDS); if (delay <= 0) return q.poll();
                    first = null; // don't retain ref while waiting
                    if (leader != null)
                        available.await(); else {
                        Thread thisThread = Thread.currentThread();
                        leader = thisThread; try {
                            available.awaitNanos(delay);
                        } finally { if (leader == thisThread)
                                leader = null;
                        }
                    }
                }
            }
        } finally { if (leader == null && q.peek() != null)
                available.signal();
            lock.unlock();
        }
    } </pre>

~~~
### get点

　整个代码的过程中并没有使用上太难理解的地方,但是有几个比较难以理解他为什么这么做的地方

#### leader元素的使用

　大家可能看到在我们的DelayQueue中有一个Thread类型的元素leader,那么他是做什么的呢,有什么用呢？

　让我们先看一下元素注解上的doc描述:

> Thread designated to wait for the element at the head of the queue.
> This variant of the [Leader-Follower pattern](https://link.jianshu.com/?t=http://www.cs.wustl.edu/~schmidt/POSA/POSA2/) serves to minimize unnecessary timed waiting.
> when a thread becomes the leader, it waits only for the next delay to elapse, but other threads await indefinitely.
> The leader thread must signal some other thread before returning from take() or poll(...), unless some other thread becomes leader in the interim.
> Whenever the head of the queue is replaced with an element with an earlier expiration time, the leader field is invalidated by being reset to null, and some waiting thread, but not necessarily the current leader, is signalled.
> So waiting threads must be prepared to acquire and lose leadership while waiting.

　上面主要的意思就是说用leader来减少不必要的等待时间,那么这里我们的DelayQueue是怎么利用leader来做到这一点的呢:

　这里我们想象着我们有个多个消费者线程用take方法去取,内部先加锁,然后每个线程都去peek第一个节点.
　如果leader不为空说明已经有线程在取了,设置当前线程等待

```
if (leader != null)
   available.await();

```

　如果为空说明没有其他线程去取这个节点,设置leader并等待delay延时到期,直到poll后结束循环

```
     else {
         Thread thisThread = Thread.currentThread();
         leader = thisThread;
         try {
              available.awaitNanos(delay);
         } finally {
              if (leader == thisThread)
                  leader = null;
         }
     }

```

#### take方法中为什么释放first元素

```
first = null; // don't retain ref while waiting

```

　我们可以看到doug lea后面写的注释,那么这段代码有什么用呢？

　想想假设现在延迟队列里面有三个对象。

*   线程A进来获取first,然后进入 else 的else ,设置了leader为当前线程A
*   线程B进来获取first,进入else的阻塞操作,然后无限期等待
*   这时在JDK 1.7下面他是持有first引用的
*   如果线程A阻塞完毕,获取对象成功,出队,这个对象理应被GC回收,但是他还被线程B持有着,GC链可达,所以不能回收这个first.
*   假设还有线程C 、D、E.. 持有对象1引用,那么无限期的不能回收该对象1引用了,那么就会造成内存泄露.
