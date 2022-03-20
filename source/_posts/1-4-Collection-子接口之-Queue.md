---
title: 1-4-Collection-子接口之-Queue.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
## 
1.4 Collection 子接口之 Queue

### 1.4.1 Queue 与 Deque 的区别

Queue是单端队列，只能从一端插入元素，另一端删除元素，实现上一般遵循 **先进先出（FIFO）** 规则。

Queue扩展了 Collection的接口，根据 **因为容量问题而导致操作失败后处理方式的不同** 可以分为两类方法: 一种在操作失败后会抛出异常，另一种则会返回特殊值（布尔值或object） 。

| Queue接口 | 抛出异常 | 返回特殊值 |
| --- | --- | --- |
| 插入队尾 | add(E e) | boolean offer(E e)  失败返回false|
| 删除队首 | remove() | Object poll() 失败返回null |
| 查询队首元素 | element() | Object peek() 失败返回null |
> 记忆方法：
低级词汇：add、remove、element 会引发异常；
高级词汇：offer（插入）、poll（都有o）、peek（都有e） ；会返回特殊值（布尔值或object） 

Deque是双端队列，在队列的两端均可以插入或删除元素。

Deque扩展了 Queue的接口, 增加了在队首和队尾进行插入和删除的方法，同样根据失败后处理方式的不同分为两类：

| Deque接口 | 抛出异常 | 返回特殊值 |
| --- | --- | --- |
| 插入队首 | addFirst(E e) | offerFirst(E e) |
| 插入队尾 | addLast(E e) | offerLast(E e) |
| 删除队首 | removeFirst() | pollFirst() |
| 删除队尾 | removeLast() | pollLast() |
| 查询队首元素 | getFirst() | peekFirst() |
| 查询队尾元素 | getLast() | peekLast() |

>事实上，Deque还提供有 push()和 pop()等其他方法，可用于模拟栈。

### 1.4.2 ArrayDeque 与 LinkedList 的区别

ArrayDeque和 LinkedList都实现了 Deque接口，两者都具有队列的功能，但两者有什么区别呢？

*   ArrayDeque是基于可变长的数组和双指针来实现，而 LinkedList则通过链表来实现。

*   ArrayDeque不支持存储 NULL数据，但 LinkedList支持。
> Qeque、Deque 都不允许存入null。否则报空指针

*   ArrayDeque是在 JDK1.6 才被引入的，而LinkedList早在 JDK1.2 时就已经存在。

*   ArrayDeque插入时可能存在扩容过程, 不过均摊后的插入操作依然为 O(1)。虽然 LinkedList不需要扩容，但是每次插入数据时均需要申请新的堆空间，均摊性能相比更慢。

>从性能的角度上，选用 ArrayDeque来实现队列要比 LinkedList更好。此外，ArrayDeque也可以用于实现栈。

###1.4.3 说一说 PriorityQueue

PriorityQueue是在 JDK1.5 中被引入的, 其与 Queue的区别在于元素出队顺序是与优先级相关的，即总是优先级最高的元素先出队。

这里列举其相关的一些要点：

*   PriorityQueue利用了二叉堆的数据结构来实现的，底层使用可变长的数组来存储数据
*   PriorityQueue通过堆元素的上浮和下沉，实现了在 O(logn) 的时间复杂度内插入元素和删除堆顶元素。
*   PriorityQueue是非线程安全的，且不支持存储 NULL和 non-comparable的对象。
*   PriorityQueue默认是小顶堆，但可以接收一个 Comparator作为构造参数，从而来自定义元素优先级的先后。
> 其实就是按优先级自定义排序

PriorityQueue在面试中可能更多的会出现在手撕算法的时候，典型例题包括堆排序、求第K大的数、带权图的遍历等，所以需要会熟练使用才行。

~~~
  PriorityQueue<Integer> objects = new PriorityQueue<>(5,new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o1-o2;
            }
        });

        objects.offer(200);
        objects.offer(1);
        objects.offer(33);
        objects.offer(888);
        objects.offer(666);
        boolean offer = objects.offer(999);
        System.out.println(offer);

        while (!objects.isEmpty()){
            System.out.println(objects.poll());
        }

~~~
###LinkedBlockingDeque
LinkedBlockingDeque是BlockingDeque接口唯一的实现类

使用它来模拟栈
~~~
        LinkedBlockingDeque<Object> objects = new LinkedBlockingDeque<>(3);
        objects.push(1);
        objects.push(2);
        objects.push(3);
        Object pop = objects.pop();

        //3
        System.out.println(pop);
~~~
