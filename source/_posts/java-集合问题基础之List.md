---
title: java-集合问题基础之List.md
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
###Arraylist 和 Vector 的区别?
ArrayList 是 List 的主要实现类，底层使用 Object[ ]存储，适用于频繁的查找工作，线程不安全 ；
Vector 是 List 的古老实现类，底层使用Object[ ] 存储，线程安全的。

### Arraylist 与 LinkedList 区别?
1、是否保证线程安全： ArrayList 和 LinkedList 都是不同步的，也就是不保证线程安全；

2、底层数据结构： Arraylist 底层使用的是`Object 数组`；LinkedList 底层使用的是 `双向链表` 数据结构（JDK1.6 之前为循环链表，JDK1.7 取消了循环。注意双向链表和双向循环链表的区别，下面有介绍到！）

3、插入和删除是否受元素位置的影响：
ArrayList 采用数组存储，所以插入和删除元素的时间复杂度受元素位置的影响。 比如：执行add(E e)方法的时候， ArrayList 会默认在将指定的元素追加到此列表的`末尾`，这种情况时间复杂度就是 O(1)。**但是如果要在指定位置 i 插入和删除元素的话（add(int index, E element)）时间复杂度就为 `O(n-i)`。因为在进行上述操作的时候集合中第 i 和第 i 个元素之后的(n-i)个元素都要执行向后位/向前移一位的操作。**

LinkedList 采用链表存储，所以，如果是在`头尾`插入或者删除元素不受元素位置的影响（add(E e)、addFirst(E e)、addLast(E e)、removeFirst() 、 removeLast()），近似 O(1)，**如果是要在指定位置 i 插入和删除元素的话（add(int index, E element)，remove(Object o)） `时间复杂度近似为 O(n)`**，因为需要先移动到指定位置再插入。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-6a5deab5e66b7c8c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



4、是否支持快速随机访问： LinkedList 不支持高效的随机元素访问，而 ArrayList 支持。快速随机访问就是通过元素的序号快速获取元素对象(对应于get(int index)方法)。


5、内存空间占用： ArrayList 的空 间浪费主要体现在在 list 列表的结尾会**预留一定的容量空间（因为会到达0.75加载因子时会自动扩容。总会有一些剩余空间的）**，**而 LinkedList 的空间花费则体现在它的每一个元素都需要消耗比 ArrayList 更多的空间（因为要存放直接后继和直接前驱以及数据）**。`LinkedList初始化不能指定初始容量`,所以也就不会自动扩容。


###补充内容:双向链表和双向循环链表
双向链表： 包含两个指针，一个 prev 指向前一个节点，一个 next 指向后一个节点。
另外推荐一篇把双向链表讲清楚的文章：https://juejin.im/post/5b5d1a9af265da0f47352f14

双向循环链表： 最后一个节点的 next 指向 head，而 head 的 prev 指向最后一个节点，构成一个环。




###补充内容:RandomAccess 接口
public interface RandomAccess {
}
查看源码我们发现实际上 RandomAccess 接口中什么都没有定义。所以，在我看来 RandomAccess 接口不过是一个标识罢了。标识什么？ 标识实现这个接口的类具有随机访问功能。

在 binarySearch（) 方法中，它要判断传入的 list 是否 RamdomAccess 的实例，如果是，调用indexedBinarySearch()方法，如果不是，那么调用iteratorBinarySearch()方法

    public static <T>
    int binarySearch(List<? extends Comparable<? super T>> list, T key) {
        if (list instanceof RandomAccess || list.size()<BINARYSEARCH_THRESHOLD)
            return Collections.indexedBinarySearch(list, key);
        else
            return Collections.iteratorBinarySearch(list, key);
    }
ArrayList 实现了 RandomAccess 接口， 而 LinkedList 没有实现。为什么呢？我觉得还是和底层数据结构有关！ArrayList 底层是数组，而 LinkedList 底层是链表。数组天然支持随机访问，时间复杂度为 O(1)，所以称为快速随机访问。**链表需要遍历到特定位置才能访问特定位置的元素，时间复杂度为 O(n)**，所以不支持快速随机访问。ArrayList 实现了 RandomAccess 接口，就表明了他具有快速随机访问功能。 RandomAccess 接口只是标识，并不是说 ArrayList 实现 RandomAccess 接口才具有快速随机访问功能的！



###说一说 ArrayList 的扩容机制吧


默认初始10  、原来的 1.5倍、第一次add才会将容量设置为10个（懒汉）；
底层使用Arrays.copy扩容；
最大容量是 Integer.Max - 8 或者 Integer.Max ；
