---
title: java-集合之ArrayList和LinkedList的区别和使用建议.md
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
1、ArrayList 基于动态数组实现的非线程安全的集合；LinkedList 基于双向链表实现的非线程安全的集合。

2、扩容问题：ArrayList 使用数组实现，无参构造函数默认初始化长度为 10，数组扩容是会将原数组中的元素重新拷贝到新数组中，长度为原来的 1.5 倍(扩容代价高)；LinkedList 不存在扩容问题，新增元素放到集合尾部，修改相应的指针节点即可。

3、LinkedList 比 ArrayList 更占内存，因为 LinkedList 为每一个节点存储了两个引用节点，一个指向前一个元素，一个指向下一个元素。

4、对于随机 index 访问的 get 和 set 方法，一般 ArrayList 的速度要优于 LinkedList。因为 ArrayList 直接通过数组下标直接找到元素；LinkedList 要移动指针遍历每个元素直到找到为止。

5、新增add和删除remove元素，一般 LinkedList 的速度要优于 ArrayList。因为 ArrayList 在新增和删除元素时，可能扩容和复制数组；LinkedList 实例化对象需要时间外，只需要修改节点指针即可。

6、LinkedList 集合不支持高效的随机访问（RandomAccess）
ArrayList 的空间浪费主要体现在在list列表的结尾预留一定的容量空间；LinkedList 的空间花费则体现在它的每一个元素都需要消耗存储指针节点对象的空间。


###使用建议
1、千万别在循环中调用 LinkedList 的 get 方法，耗时会让你崩溃。最好采用Iterator或者foreach的方式遍历，效率最高，因为foreach编译后就是使用Iterator的。

思考：

arrayList add 10000000 cost time: 3293；linkedList add 10000000 cost time: 1337
arrayList add 1000000  cost time: 22  ；   linkedList add 1000000   cost time: 1011
跑另外一组数据，size 设为 1000 * 1000，得出当size增加，ArrayList 的 add操作的累计时间增长更快


代码例子中，"新增和删除元素，一般 LinkedList 的速度要优于 ArrayList" 并不成立，可以思考一下原因。
 
理论上 set、get、fori循环遍历 这些设计到index索引位置的方法（随机访问） ArrayList比LinkedList快。而add、remove等移动元素位置的方法LinkedList较快。
但是注意：无论是fori、foreach、iterator。对于相同元素的两个遍历。都是ArrayList快


###测试例子
~~~
package com.springboot.study.demo1;

import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;


public class Test {
    public static void main(String[] args) {
        ArrayList<Integer> arrayList = new ArrayList<Integer>();
        LinkedList<Integer> linkedList = new LinkedList<Integer>();
        int size = 10000 * 1000;
        int index = 5000 * 1000;

        System.out.println("arrayList add " + size);
        addData(arrayList, size);
        System.out.println("linkedList add " +  + size);
        addData(linkedList, size);
        System.out.println();

        System.out.println("arrayList get " + index + " th");
        getIndex(arrayList, index);
        System.out.println("linkedList get " + index + " th");
        getIndex(linkedList, index);
        System.out.println();

        System.out.println("arrayList set " + index + " th");
        setIndex(arrayList, index);
        System.out.println("linkedList set " + index + " th");
        setIndex(linkedList, index);
        System.out.println();

        System.out.println("arrayList add " + index + " th");
        addIndex(arrayList, index);
        System.out.println("linkedList add " + index + " th");
        addIndex(linkedList, index);
        System.out.println();

        System.out.println("arrayList remove " + index + " th");
        removeIndex(arrayList, index);
        System.out.println("linkedList remove " + index + " th");
        removeIndex(linkedList, index);
        System.out.println();

        System.out.println("arrayList remove Object " + index);
        removeObject(arrayList, (Object)index);
        System.out.println("linkedList remove Object " + index);
        removeObject(linkedList, (Object)index);
        System.out.println();

        System.out.println("arrayList add");
        add(arrayList);
        System.out.println("linkedList add");
        add(linkedList);
        System.out.println();

        System.out.println("arrayList foreach");
        foreach(arrayList);
        System.out.println("linkedList foreach");
        foreach(linkedList);
        System.out.println();

        System.out.println("arrayList forSize");
        forSize(arrayList);
        System.out.println("linkedList forSize 慢到怀疑人生 ......");
		forSize(linkedList);
        System.out.println("cost time: ...");
        System.out.println();

        System.out.println("arrayList iterator");
        ite(arrayList);
        System.out.println("linkedList iterator");
        ite(linkedList);
    }

    private static void addData(List<Integer> list, int size) {
        long s1 = System.currentTimeMillis();
        for (int i = 0; i <size; i++) {
            list.add(i);
        }
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void getIndex(List<Integer> list, int index) {
        long s1 = System.currentTimeMillis();
        list.get(index);
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void setIndex(List<Integer> list, int index) {
        long s1 = System.currentTimeMillis();
        list.set(index, 1024);
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void addIndex(List<Integer> list, int index) {
        long s1 = System.currentTimeMillis();
        list.add(index, 1024);
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void removeIndex(List<Integer> list, int index) {
        long s1 = System.currentTimeMillis();
        list.remove(index);
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void removeObject(List<Integer> list, Object obj) {
        long s1 = System.currentTimeMillis();
        list.remove(obj);
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void add(List<Integer> list) {
        long s1 = System.currentTimeMillis();
        list.add(1024);
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void foreach(List<Integer> list) {
        long s1 = System.currentTimeMillis();
        for (Integer i : list) {
            //do nothing
        }
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void forSize(List<Integer> list) {
        long s1 = System.currentTimeMillis();
        int size = list.size();
        for (int i = 0; i <size; i++) {
            list.get(i);
        }
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }

    private static void ite(List<Integer> list) {
        long s1 = System.currentTimeMillis();
        Iterator<Integer> ite = list.iterator();
        while (ite.hasNext()) {
            ite.next();
        }
        long s2 = System.currentTimeMillis();
        System.out.println("cost time: " + (s2-s1));
    }


}
~~~
