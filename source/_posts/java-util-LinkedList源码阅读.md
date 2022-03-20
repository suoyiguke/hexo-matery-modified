---
title: java-util-LinkedList源码阅读.md
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
title: java-util-LinkedList源码阅读.md
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

java.util.LinkedList#node 方法就是LinkedList遍历寻址的核心方法。
add、remove、set、get 都有用到这个方法

~~~
public void add(int index, E element) {
       //判断索引是否越界
        checkPositionIndex(index);
 
        if (index == size)
        //如果索引值等于链表大小，则直接在链尾添加元素
            linkLast(element);
        else
            linkBefore(element, node(index));
}
 
//根据索引获取节点，因为是链表，不像数组，在内存中并不是一块连续的位置存储，不能根据索引直接取到值，需要从头部或者尾部一个个向下找
Node<E> node(int index) {
    //size >> 1表示移位，指除以2的1次方
    if (index < (size >> 1)) {//如果索引比链表的一半小
        Node<E> x = first;//设x为头节点,表示从头节点开始遍历
        for (int i = 0; i < index; i++)//因为只需要找到index处，所以遍历到index处就可以停止
            x = x.next;//从第一个节点开始向后移动，直到移动到index前一个节点就能找到index处的节点
        return x;
    } else {//如果索引比链表的一半大
        Node<E> x = last;//设x为尾部节点,表示从最后一格节点开始遍历
        for (int i = size - 1; i > index; i--)
            x = x.prev;//从最后一个节点开始向前移动，直到移动到index后一个节点就能找到index处的节点
        return x;
    }
}
 
void linkBefore(E e, Node<E> succ) {
 
        //获取index 节点的上一个节点
        final Node<E> pred = succ.prev;
 
        //新增一个节点，prev指向pred,e为新加元素，next指向succ节点
        final Node<E> newNode = new Node<>(pred, e, succ);
 
        //succ的prev指向新节点
        succ.prev = newNode;
 
        //如果插入节点的上一个节点引用为空
        if (pred == null)
 
        //头部节点设为新节点
            first = newNode;
        else
        //原始index的上一个节点的next 设为新节点
            pred.next = newNode;
        //链表长度+1
        size++;
        modCount++;
}
~~~
