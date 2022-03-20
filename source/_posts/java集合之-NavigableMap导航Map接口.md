---
title: java集合之-NavigableMap导航Map接口.md
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
https://blog.csdn.net/cgsyck/article/details/108462189

###一、返回key
####1、根据指定key大小返回符合要求的key
higherKey 返回最接近的大于指定key的key
~~~
        NavigableMap<Integer,Integer> original = new TreeMap<Integer,Integer>();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);

        Integer ceilingKey = original.higherKey(2);
        System.out.println(ceilingKey);//3
~~~

lowerKey 返回最接近的小于指定key的key
~~~
        NavigableMap<Integer,Integer> original = new TreeMap<Integer,Integer>();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);

        Integer ceilingKey = original.lowerKey(2);
        System.out.println(ceilingKey);//1
~~~

ceilingKey 返回最接近的大于等于指定key的key
~~~
        NavigableMap<Integer,Integer> original = new TreeMap<Integer,Integer>();
        original.put(1, 1);
        original.put(3, 3);
        original.put(4, 4);

        System.out.println(original.ceilingKey(2));//3
        System.out.println(original.ceilingKey(3));//3
~~~

floorKey返回最接近的小于等于指定key的key
~~~
        NavigableMap<Integer,Integer> original = new TreeMap<Integer,Integer>();
        original.put(1, 1);
        original.put(3, 3);
        original.put(4, 4);

        System.out.println(original.floorKey(2));//1
        System.out.println(original.floorKey(3));//3
~~~


####2、返回倒序的key集合
descendingKeySet 返回key倒序NavigableSet
~~~
        NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);
        original.put(4, 4);
        original.put(5, 5);
        //[5, 4, 3, 2, 1] 返回key倒序排列的key集合NavigableSet
        System.out.println(original.descendingKeySet());
~~~
###3、返回第一个key
firstKey
~~~
        NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);
        //1 获取第一个key
        System.out.println(original.firstKey());
~~~
###4、返回第一个key、最后一个key
firstKey、lastKey
~~~
    NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);
        //1 获取第一个key
        System.out.println(original.firstKey());
        //3 获取最后一个key
        System.out.println(original.lastKey());
~~~



###二、返回Map
####1、根据key大小返回符合要求的Map视图

1、tailMap 返回大于（可选择是否包含等于）指定key的Map视图
~~~
        NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);

        SortedMap headmap1 = original.tailMap(1);
        //{1=1, 2=2, 3=3} 默认true包含等于
        System.out.println(headmap1);

        //{1=1, 2=2, 3=3} fasle不包含
        NavigableMap headmap2 = original.tailMap(1, false);
        System.out.println(headmap2);
~~~
2、headMap 返回小于（可选择是否包含等于）指定key的Map视图
~~~
        NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);

        SortedMap headmap1 = original.headMap(3);
        // {1=1, 2=2} 默认false，不包含等于
        System.out.println(headmap1);

        //{1=1, 2=2, 3=3} true包含等于
        NavigableMap headmap2 = original.headMap(3, true);
        System.out.println(headmap2);

~~~

>注意tailMap 、headMap  的inclusive默认值是不同的；tailMap默认true包含等于，headMap默认false，不包含等于。


####2、返回符合指定范围key大小的Map视图
subMap
~~~
        NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);
        original.put(4, 4);
        original.put(5, 5);

        //{2=2, 3=3} 默认fromInclusive为true， toInclusive为 false；
        System.out.println(original.subMap(2, 4));

        //{2=2, 3=3, 4=4}
        System.out.println(original.subMap(2, true, 4, true));
~~~


####3、返回key倒序排列的NavigableMap
descendingMap 
~~~
        NavigableMap original = new TreeMap();
        original.put(1, 1);
        original.put(2, 2);
        original.put(3, 3);
        original.put(4, 4);
        original.put(5, 5);
        //{5=5, 4=4, 3=3, 2=2, 1=1} 返回key倒序排列的NavigableMap
        NavigableMap navigableMap = original.descendingMap();

        //操作会互相影响
        navigableMap.put(6,6);
        //{1=1, 2=2, 3=3, 4=4, 5=5, 6=6}
        System.out.println(original);

        //操作会互相影响
        original.put(7,7);
        //{7=7, 6=6, 5=5, 4=4, 3=3, 2=2, 1=1}
        System.out.println(navigableMap);
~~~
>注意：仍然是同一个map，操作会互相影响。
