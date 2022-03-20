---
title: java-有序Map之TreeMap的使用.md
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
>谦虚使人进步

想要了解一个类，就可以从它实现的接口和继承的父类开始。我们可以看到TreeMap实现了java.util.NavigableMap接口，NavigableMap它又继承了排序Map接口 java.util.SortedMap，因此TreeMap具有排序能力；其次，TreeMap实现了Cloneable和Serializable接口，它也具备克隆和序列化能力


![image.png](https://upload-images.jianshu.io/upload_images/13965490-cb04e714a1912fd8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


TreeMap底层由`红黑树`实现，按照`Key的自然顺序升序`或者实现Comprator接口进行`自定义排序`。且TreeMap的排序特性只作用在key上。如果需要value也跟着排序就需要使用一些别的手段。

###排序特性
######按key排序
默认按key升序排列
~~~
package com.springboot.study.demo1;
import java.util.*;

public class Test {
    public static void main(String[] args) {

        TreeMap<String, String> treeMap = new TreeMap<String, String>() {{
            put("3", "1");
            put("1", "3");
            put("2", "2");

        }};

        for (String s : treeMap.keySet()) {
            System.out.println(s+"==>"+treeMap.get(s));
        }

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ae30bf8423101df9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


按key降序排列
~~~
package com.springboot.study.demo1;

import java.util.*;

public class Test {
    public static void main(String[] args) {

        TreeMap<String, String> treeMap = new TreeMap<String, String>(new Comparator<String>() {
            @Override
            public int compare(String o1, String o2) {
                return o2.compareTo(o1);
            }
        }) {{
            put("3", "1");
            put("1", "2");
            put("2", "3");

        }};

        for (String s : treeMap.keySet()) {
            System.out.println(s + "==>" + treeMap.get(s));
        }

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f91c78019a65d7ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######按value排序
如果需要value也跟着排序就需要使用一些别的手段。当然HashMap的value排序也可以使用这种方法

将Map转为 List<Map.Entry>，然后使用java.util.Collections工具类来排序。当然这种方法也适用于HashMap

~~~
package com.springboot.study.demo1;

import java.util.*;
import java.util.stream.Collectors;

public class Test {
    public static void main(String[] args) {
        Map<String, String> treeMap = new HashMap<String, String>() {{
            put("3", "1");
            put("1", "2");
            put("2", "3");

        }};

        //将Map转为 List<Map.Entry>
        List<Map.Entry<String, String>> list = new ArrayList<>(treeMap.entrySet());
        //按照
        Collections.sort(list,new Comparator<Map.Entry<String,String>>() {
            //升序排序
            public int compare(Map.Entry<String, String> o1, Map.Entry<String, String> o2) {
                return o1.getValue().compareTo(o2.getValue());
            }
        });


        for (Map.Entry<String, String> e: list) {
            System.out.println(e.getKey()+"==>"+e.getValue());
        }

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-831110e1b5371228.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###性能特性

- TreeMap的优势在于能够实现`自定义排序功能`，但是性能要比HashMap和LinkedHashMap差。它的 containsKey 、get 、 put 、remove 方法的时间复杂度是 log(n)

- 虽然LinkedHashMap也是有序的，但是LinkedHashMap内元素顺序只和插入顺序有关，无法进行自定义排序

