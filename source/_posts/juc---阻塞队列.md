---
title: juc---阻塞队列.md
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
title: juc---阻塞队列.md
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
###什么是阻塞队列
- 当队列是空的，从队列中获取元素的操作将会被阻塞。直到其他线程往空的队列里插入新的元素的时候解除阻塞，继续获取
- 当队列是满的，从队列中添加元素的操作将会被阻塞。直到其他线程从队列里移除一个或多个元素或者完全清空的时候解除阻塞，继续新增


###为什么需要阻塞队列
好处是我们不需要关心什么时候需要阻塞线程，什么时候唤醒线程，因为这一切BlockingQueue都给你一手包办了。

###阻塞队列接口
java.util.concurrent.BlockingQueue 即是阻塞队列接口，类似于ArrayList的接口是java.util.List。BlockingQueue 接口继承于Queue。Queue和我们熟悉的List、Set都是Collection接口的子接口

![image.png](https://upload-images.jianshu.io/upload_images/13965490-6f2db45d1f8fd636.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######BlockingQueue 接口的常用方法
![image.png](https://upload-images.jianshu.io/upload_images/13965490-be0dd6b4b2555316.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 抛出异常的方法。 添加元素方法boolean add(E e) 和移除元素方法E remove() `有被移除的元素当返回值`、 E element()  检查方法，查看队列的队首元素，并不删除。如果队列为空则抛出异常  java.util.NoSuchElementException
~~~
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
public class Test {
    public static void main(String[] args) {

        BlockingQueue<Integer> blockingQueue = new ArrayBlockingQueue(3);
        blockingQueue.add(1);
        blockingQueue.add(2);
        blockingQueue.add(3);
        //队列满了，报错 java.lang.IllegalStateException: Queue full
        //blockingQueue.add(4);

        // 值为1  队列是先进先出的
        System.out.println(blockingQueue.remove());
        //2
        System.out.println(blockingQueue.remove());
        //3
        System.out.println(blockingQueue.remove());
        //队列空了，报错 java.util.NoSuchElementException
        //System.out.println(blockingQueue.remove());

        //查看队列的队首元素，并不删除。如果队列为空则抛出异常  java.util.NoSuchElementException
        //System.out.println(blockingQueue.element());

    }
}
~~~
- 引发阻塞的方法。既然是阻塞队列，那么可能引发阻塞的 void put(E e) throws InterruptedException 添加方法和E take() throws InterruptedException移除方法 是最常用的！
~~~
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
public class Test {
    public static void main(String[] args) throws InterruptedException {

        BlockingQueue<Integer> blockingQueue = new ArrayBlockingQueue(3);
        blockingQueue.put(1);
        blockingQueue.put(2);
        blockingQueue.put(3);
        //队列满了，再使用put()方法添加元素，引发阻塞
        //blockingQueue.put(4);

        System.out.println(blockingQueue.take());
        System.out.println(blockingQueue.take());
        System.out.println(blockingQueue.take());
        //队列空了，再使用take()方法移除元素，引发阻塞
        //System.out.println(blockingQueue.take());

    }
}
~~~

- 返回特殊值的方法（即不会引发阻塞也不会抛出异常）。boolean offer(E e) 添加方法和E poll() 移除方法，还有E peek()检查方法，查看队列的队首元素，并不删除。如果队列为空则返回null
~~~
import java.util.concurrent.ArrayBlockingQueue;import java.util.concurrent.BlockingQueue;
public class Test {
    public static void main(String[] args) {

        BlockingQueue<Integer> blockingQueue = new ArrayBlockingQueue(3);
        System.out.println(blockingQueue.offer(1));
        System.out.println(blockingQueue.offer(2));
        System.out.println(blockingQueue.offer(3));
        //队列满了，offer()添加方法返回false
        System.out.println(blockingQueue.offer(4));
        //返回队列首，这里打印1
        System.out.println(blockingQueue.peek());

        System.out.println(blockingQueue.poll());
        System.out.println(blockingQueue.poll());
        System.out.println(blockingQueue.poll());
        //队列空了，poll()移除方法返回 null
        System.out.println(blockingQueue.poll());

        //返回队列首，若果队列为空则返回null
        System.out.println(blockingQueue.peek());
    }
}
~~~

- 引发阻塞,设定等待时间。但是超时则返回特殊值`（引发阻塞和返回特殊值的结合）`。 boolean offer(E e, long timeout, TimeUnit unit) throws InterruptedException  方法阻塞指定时间，如果期间有空间那么返回true，插入成功。如果时间到了仍然没有空间则返回false。E poll(long timeout, TimeUnit unit) throws InterruptedException 方法在指定空间内如果队列中有元素则返回元素，否则返回null
~~~
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

public class Test {
    public static void main(String[] args) throws InterruptedException {

        BlockingQueue<Integer> blockingQueue = new ArrayBlockingQueue(3);
        System.out.println(blockingQueue.offer(1));
        System.out.println(blockingQueue.offer(2));
        System.out.println(blockingQueue.offer(3));
        //队列满了，再使用offer()方法添加元素，引发阻塞。等待1秒后如果仍然没有空间则返回false，有空间的话插入成功则返回true
        System.out.println( blockingQueue.offer(4,1,TimeUnit.SECONDS));


        System.out.println(blockingQueue.poll());
        System.out.println(blockingQueue.poll());
        System.out.println(blockingQueue.poll());
        //队列空了，再使用poll()方法移除元素，引发阻塞。1秒后如果有元素了，那么返回该元素。否则返回null
        System.out.println(blockingQueue.poll(1,TimeUnit.SECONDS));

    }
}
~~~

###所有阻塞队列
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9a838b0f2236d8f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######`掌握`ArrayBlockingQueue
由`数组结构`组成的`有界`阻塞队列
~~~
BlockingQueue blockingQueue = new ArrayBlockingQueue(3,true,new ArrayList());
~~~
######`掌握`LinkedBlockingQueue
由`链表结构`组成的`有界`(大小默认为Integer.MAX_VALUE)阻塞队列
~~~
 BlockingQueue<Object> blockingQueue = new LinkedBlockingQueue<>(new ArrayList<>());
~~~

######PriorityQueue
支持优先级排序的无界阻塞队列
~~~
BlockingQueue<Object> blockingQueue = new PriorityBlockingQueue<>();
~~~

######DelayQueue
使用优先级队列实现的延迟无界阻塞队列
~~~
BlockingQueue blockingQueue = new DelayQueue();
~~~

######`掌握`SynchronousQueue
`不存储元素`的阻塞队列，也即`单个元素`的阻塞队列
~~~
BlockingQueue blockingQueue = new SynchronousQueue();
~~~
######LinkedTransferQueue
由链表组成的无界阻塞队列
~~~
BlockingQueue blockingQueue = new LinkedTransferQueue();
~~~
######LinkedBlockingDeque
由链表组成的双向阻塞队列
Deque  表示 Double Queue
~~~
BlockingQueue blockingQueue = new LinkedBlockingDeque();
~~~
