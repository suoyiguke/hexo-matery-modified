---
title: Disruptor-高性能队列.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: Disruptor-高性能队列.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
The LMAX Disruptor is a high performance inter-thread messaging library. It grew out of LMAX’s research into concurrency, performance and non-blocking algorithms and today forms a core part of their Exchange’s infrastructure.



https://github.com/LMAX-Exchange/disruptor
https://lmax-exchange.github.io/disruptor/user-guide/index.html#user-guide-models

比jdk ArrayBlockingQueue性能高几倍


###性能

disruptor是用于一个JVM中多个线程之间的消息队列，作用与ArrayBlockingQueue有相似之处，但是disruptor从功能、性能都远好于ArrayBlockingQueue，当多个线程之间传递大量数据或对性能要求较高时，可以考虑使用disruptor作为ArrayBlockingQueue的替代者。

官方也对disruptor和ArrayBlockingQueue的性能在不同的应用场景下做了对比，本文列出其中一组数据，数据中P代表producer，C代表consumer，ABS代表ArrayBlockingQueue：

![image](https://upload-images.jianshu.io/upload_images/13965490-6a5a35367c2c6766.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

完整的官方性能测试数据在Performance Results · LMAX-Exchange/disruptor Wiki可以看到，性能测试的代码已经包含在disruptor的代码中，你完全可以git下来在自己的主机上测试一下看看

> https://github.com/LMAX-Exchange/disruptor/wiki/Performance-Results





另一方面，ABQ的所有操作都是互斥的，这点其实不是必要的，尤其像put和get操作，没必要共享一个lock，完全可以降低锁的粒度提高性能。

disruptor则与之不同：

disruptor使用了CAS机制同步线程，线程同步代价小于lock

disruptor遵守single writer原则，一块内存对应单个线程，不仅produce和consume不是互斥的，多线程的produce也不是互斥的

###伪共享

伪共享一直是一个比较高级的话题，Doug lea在JDK的Concurrent使用了大量的缓存行（cache line）机制避免伪共享，disruptor也是用了这样的机制。但是对于广大的码农而言，实际工作中我们可能很少会需要使用这样的机制。毕竟对于大部分人而言，与避免伪共享带来的性能提升而言，优化工程架构，算法，io等可能会给我们带来更大的性能提升。所以本文只简单提到这个话题，并不深入讲解，毕竟我也没有实际的应用经验去讲解这个话题。




###log4j 2

以下一段文字引用自Apache log4j 2官网，这段文字足以说明disruptor对log4j 2的性能提升的巨大贡献。

Log4j 2 contains next-generation Asynchronous Loggers based on the LMAX Disruptor library. In multi-threaded scenarios Asynchronous Loggers have 18 times higher throughput and orders of magnitude lower latency than Log4j 1.x and Logback.

log4j2性能的优越主要体现在异步日志记录方面，以下两个图片摘自官网分别从吞吐率和响应时间两个方面体现了log4j2异步日志性能的强悍。






###使用

~~~
<dependency>
  <groupId>com.lmax</groupId>
  <artifactId>disruptor</artifactId>
  <version>3.4.2</version>
</dependency>
~~~

~~~
package com.lmax.disruptor.examples.objectevent;
import com.lmax.disruptor.EventHandler;
import java.util.concurrent.atomic.AtomicLong;
public class ClearingEventHandler<T> implements EventHandler<ObjectEvent<T>>
{


    protected volatile long processed;
    protected AtomicLong atomicLong = new AtomicLong(0);

    protected volatile boolean endOfBatch = false;


    @Override
    public void onEvent(ObjectEvent<T> event, long sequence, boolean endOfBatch)
    {

            this.endOfBatch = endOfBatch;
            atomicLong.incrementAndGet();
            processed = sequence;
            System.out.println("event.get()" + event.getValue());
            System.out.println("sequence" + sequence);
            System.out.println("endOfBatch" + endOfBatch);

    }
}
~~~
~~~
package com.lmax.disruptor.examples.objectevent;

import com.lmax.disruptor.EventFactory;

class ObjectEvent<T>
{

    private String value;

    public void set(final String value)
    {
        this.value = value;
    }

    public String getValue()
    {
        return value;
    }


    public static final EventFactory<ObjectEvent> FACTORY = () -> new ObjectEvent();
}
~~~

~~~
package com.lmax.disruptor.examples.objectevent;

import com.lmax.disruptor.EventTranslator;
import com.lmax.disruptor.RingBuffer;
import com.lmax.disruptor.dsl.Disruptor;
import com.lmax.disruptor.util.DaemonThreadFactory;

@SuppressWarnings("unchecked")
public class Main
{

    public static void main(String[] args)
    {
        Disruptor<ObjectEvent<String>> disruptor = new Disruptor<>(
                () -> new ObjectEvent<>(), 1024, DaemonThreadFactory.INSTANCE);


        //消费
        ClearingEventHandler handler1 = new ClearingEventHandler();
        ClearingEventHandler handler2 = new ClearingEventHandler();
        disruptor.handleEventsWith(handler1,handler2);

        //生产
        RingBuffer<ObjectEvent<String>> buffer = disruptor.start();
        int eventCount = 10000;
        for (int i = 0; i < eventCount; i++)
        {
            long sequence = buffer.next();
            ObjectEvent<String> stringObjectEvent = buffer.get(sequence);
            stringObjectEvent.set("test:"+i);
            buffer.publish(sequence);
        }


        while (!handler1.endOfBatch||!handler2.endOfBatch)
        {
            try
            {
                Thread.sleep(1);
            }
            catch (InterruptedException e)
            {
                e.printStackTrace();
            }
        }
    }

}

~~~
