---
title: 优先队列-PriorityQueue.md
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
title: 优先队列-PriorityQueue.md
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
可以自定义排序的List。类比TreeMap，可以自定义排序的Map，TreeSet，可自定义排序的Set
使用：
        PriorityQueue<ZskAccessoriesListDtoError> objects = new PriorityQueue<>(Comparator.comparing(ZskAccessoriesListDtoError::getRowNum, Comparator.nullsLast(Comparator.naturalOrder())));




- PriorityQueue使用跟普通队列一样，唯一区别是PriorityQueue会根据排序规则决定谁在队头，谁在队尾。

- offer 入队
- poll 出队

**1、默认按元素自然顺序排序**
~~~
package com.study;


import java.util.PriorityQueue;

public class Test {
    public static void main(String[] args) {

        PriorityQueue priorityQueue = new PriorityQueue();
        System.out.println(priorityQueue.offer(11));
        System.out.println(priorityQueue.offer(2));
        System.out.println(priorityQueue.offer(3));
        System.out.println(priorityQueue.offer(14));
        System.out.println(priorityQueue.offer(1));

        int size = priorityQueue.size();
        for (int i = 0; i <size; i++) {
            System.out.println(priorityQueue.poll());
        }

    }
}

~~~


**2、自定义排序**

PriorityQueue排序可自定义

- 添加元素的类实现了Comparable接口，确保元素是可排序的对象
- 或者创建PriorityQueue时实现Comparator接口

~~~
package com.hankcs.demo;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Comparator;
import java.util.PriorityQueue;

@Data
@AllArgsConstructor
public class Student {
    private String name;
    private int score;

    public static void main(String[] args) {
        //通过改造器指定排序规则
        PriorityQueue<Student> q = new PriorityQueue<Student>(new Comparator<Student>() {
            @Override
            public int compare(Student o1, Student o2) {
                //按照分数低到高，分数相等按名字
                if(o1.getScore() == o2.getScore()){
                    return o1.getName().compareTo(o2.getName());
                }
                return o1.getScore() - o2.getScore();
            }
        });
        q.offer(new Student("a", 100));
        q.offer(new Student("b", 120));
        q.offer(new Student("c", 70));
        q.offer(new Student("d", 90));
        q.offer(new Student("f", 90));

        System.out.println(q.poll());
        System.out.println(q.poll());
        System.out.println(q.poll());
        System.out.println(q.poll());
        System.out.println(q.poll());
    }
}

~~~



**3、源码分析**
- 不可入队 null
- 没有加锁，不是线程安全的；保证线程安全可以使用PriorityBlockingQueue 类
- 负载因子为1， i>=queue.length；超过容量就扩容
- 初始容量11
- 无参构造；直接会创建一个长度为11的Object[]
-  扩容和ArrayList差不多，为原来的1.5倍；但如果容量大于等于64时就 2倍+2；
- 也是使用 Arrays.copyOf()方法完成扩容

###应用
1、按时间戳做优先队列的排序标识。可以做到按过期时间消费
