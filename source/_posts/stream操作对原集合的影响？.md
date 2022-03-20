---
title: stream操作对原集合的影响？.md
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
1、arrayList内部复合类型
修改符合类型对象数据会影响原来的。毕竟是一个对象
~~~
        ArrayList<JgWarehouseOrder> arrayList = new ArrayList();
        JgWarehouseOrder order1 = new JgWarehouseOrder();
        order1.setId(1L);
        arrayList.add(order1);

        List<JgWarehouseOrder> collect = arrayList.stream().map(e -> e.setId(e.getId() + 1)).collect(toList());
        //2
        System.out.println(arrayList);
        //2
        System.out.println(collect);
~~~

2、arrayList内部是Integer，不会修改到原来的
~~~
       ArrayList<Integer> arrayList = new ArrayList();
        arrayList.add(1);
        List<Integer> collect = arrayList.stream().map(e -> e + 1).collect(toList());

        //1
        System.out.println(arrayList);
        //2
        System.out.println(collect);
~~~

3、arrayList内部是String，不会修改到原来的

~~~
       ArrayList<String> arrayList = new ArrayList();
        arrayList.add("1");
        List<String> collect = arrayList.stream().map(e -> e + "xxx").collect(toList());

        //1
        System.out.println(arrayList);
        //1xxx
        System.out.println(collect);
~~~


4、直接在循环里给原集合add元素是不安全的
