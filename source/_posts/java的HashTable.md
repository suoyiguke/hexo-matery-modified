---
title: java的HashTable.md
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
title: java的HashTable.md
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

1、Hashtable 继承于Dictionary，实现了Map、Cloneable、java.io.Serializable接口。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-29eea496c74b7f7b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、Hashtable 的方法都是**同步**的，这意味着它是线程安全的。看看它的put方法
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7e3481b5a82c6757.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3 、它的key、value都不可以为null。如果put入为空会报空指针
![image.png](https://upload-images.jianshu.io/upload_images/13965490-52773b48942b8b82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、默认构造器指定的 初始容量为11，加载因子为0.75
![image.png](https://upload-images.jianshu.io/upload_images/13965490-af5c28c41e0873f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
即当 元素个数 超过 容量长度的0.75倍 时，进行扩容

扩容增量：2\*原数组长度+1
如 HashTable的容量为11，一次扩容后是容量为23
0.75*11 = 8.25，容量为9时会扩容

**扩容前**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8b0b9e180f96f557.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**扩容后**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a3306eb494957bf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###扩容测试代码
~~~
import java.util.Enumeration;
import java.util.Hashtable;

public class Test2 {
    public static void main(String[] args) throws InterruptedException {


        Hashtable<Object, Object> hashtable = new Hashtable<>();
        for (int i = 1; i <=7 ; i++) {
            hashtable.put(i,i);

        }
        hashtable.put(8,8);
        Enumeration<Object> elements = hashtable.elements();
        System.out.println(elements);

        System.out.println("扩容");
        hashtable.put(9,9);
        elements = hashtable.elements();
        System.out.println(elements);



    }

}
~~~
