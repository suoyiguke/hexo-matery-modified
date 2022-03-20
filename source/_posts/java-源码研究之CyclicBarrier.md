---
title: java-源码研究之CyclicBarrier.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java源码分析
categories: java源码分析
---
---
title: java-源码研究之CyclicBarrier.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java源码分析
categories: java源码分析
---
###先看看他的类属性

~~~
/** The number of parties */
private final int parties;
~~~
parties是不可变int类型变量，在CyclicBarrier构造时会进行赋值。即是达到屏障点的线程数量
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0f84c7aed34362b4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
/* The command to run when tripped */
private final Runnable barrierCommand;
~~~
barrierCommand也是不可变的Runnable 类型，到达屏障点之后需要回调；在构造函数被初始化，可以为null

~~~
    /**
     * Number of parties still waiting. Counts down from parties to 0
     * on each generation.  It is reset to parties on each new
     * generation or when broken.
     */
    private int count;
~~~
count是可变的int，在构造器中被赋值为parties。它会一直做减1操作，直到为0就打破屏障

~~~
    /** The lock for guarding barrier entry */
    private final ReentrantLock lock = new ReentrantLock();
    /** Condition to wait on until tripped */
    private final Condition trip = lock.newCondition();
~~~
CyclicBarrier是通过 ReentrantLock和Condition 的 await-signal机制实现的 ；我的这篇文章https://www.jianshu.com/p/19ce14c2e896有对该机制的说明和使用


###看看方法
######1、解析cyclicBarrier.await() 

可以发现调用的是dowait()方法实现
~~~
    public int await() throws InterruptedException, BrokenBarrierException {
        try {
            return dowait(false, 0L);
        } catch (TimeoutException toe) {
            throw new Error(toe); // cannot happen
        }
    }
~~~

那么来看dowait()
~~~

    /**
     * Main barrier code, covering the various policies.
     */
    private int dowait(boolean timed, long nanos)
        throws InterruptedException, BrokenBarrierException,
               TimeoutException {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
            final Generation g = generation;

            if (g.broken)
                throw new BrokenBarrierException();

            if (Thread.interrupted()) {
                breakBarrier();
                throw new InterruptedException();
            }

            int index = --count;
            if (index == 0) {  // tripped
                boolean ranAction = false;
                try {
                    final Runnable command = barrierCommand;
                    if (command != null)
                        command.run();
                    ranAction = true;
                    nextGeneration();
                    return 0;
                } finally {
                    if (!ranAction)
                        breakBarrier();
                }
            }

            // loop until tripped, broken, interrupted, or timed out
            for (;;) {
                try {
                    if (!timed)
                        trip.await();
                    else if (nanos > 0L)
                        nanos = trip.awaitNanos(nanos);
                } catch (InterruptedException ie) {
                    if (g == generation && ! g.broken) {
                        breakBarrier();
                        throw ie;
                    } else {
                        // We're about to finish waiting even if we had not
                        // been interrupted, so this interrupt is deemed to
                        // "belong" to subsequent execution.
                        Thread.currentThread().interrupt();
                    }
                }

                if (g.broken)
                    throw new BrokenBarrierException();

                if (g != generation)
                    return index;

                if (timed && nanos <= 0L) {
                    breakBarrier();
                    throw new TimeoutException();
                }
            }
        } finally {
            lock.unlock();
        }
    }
~~~

1、这段代码可以看出 count 减至0时，当前线程回去执行回调的Runnable 接口。也就是最后一个到达屏障点的线程会去执行回调！
~~~
        int index = --count;
            if (index == 0) {  // tripped
                boolean ranAction = false;
                try {
                    final Runnable command = barrierCommand;
                    if (command != null)
                        command.run();
                    ranAction = true;
                    nextGeneration();
                    return 0;
                } finally {
                    if (!ranAction)
                        breakBarrier();
                }
            }
~~~


2、nextGeneration()

- 通知恢复trip上所有的等待线程
- count 减至0了，重新将parties赋值给count。这样CyclicBarrier才能重复使用
- 开启一个新的Generation

~~~
    /**
     * Updates state on barrier trip and wakes up everyone.
     * Called only while holding lock.
     */
    private void nextGeneration() {
        // signal completion of last generation
        trip.signalAll();
        // set up next generation
        count = parties;
        generation = new Generation();
    }

~~~

3、调用breakBarrier()方法来打破屏障唤醒所有到达屏障的等待线程的，这个方法在ranAction 为false时调用

- 打破屏障，将generation.broken设为true
- count 减至0了，重新将parties赋值给count。这样CyclicBarrier才能重复使用
- 通知恢复trip上所有的等待线程
~~~
   /**
     * Sets current barrier generation as broken and wakes up everyone.
     * Called only while holding lock.
     */
    private void breakBarrier() {
        generation.broken = true;
        count = parties;
        trip.signalAll();
    }

~~~
