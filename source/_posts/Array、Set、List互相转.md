---
title: Array、Set、List互相转.md
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
1. 数组转化为List：
~~~
String[] strArray= new String[]{"Tom", "Bob", "Jane"};
List strList= Arrays.asList(strArray);
 ~~~
List转数组
~~~
toArray()
~~~


2. 数组转Set
~~~
String[] strArray= new String[]{"Tom", "Bob", "Jane"}; 
Set<String> staffsSet = new HashSet<>(Arrays.asList(staffs));
 
staffsSet.add("Mary"); // ok
staffsSet.remove("Tom"); // ok
 ~~~
3. List转Set
~~~
String[] staffs = new String[]{"Tom", "Bob", "Jane"}; 
List staffsList = Arrays.asList(staffs);
Set result = new HashSet(staffsList);
 ~~~
4. set转List
~~~
String[] staffs = new String[]{"Tom", "Bob", "Jane"};
Set<String> staffsSet = new HashSet<>(Arrays.asList(staffs));
List<String> result = new ArrayList<>(staffsSet);
~~~

 

