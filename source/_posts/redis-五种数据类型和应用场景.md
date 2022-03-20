---
title: redis-五种数据类型和应用场景.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis-五种数据类型和应用场景.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
###String（字符串）



可以是字符串、整数或者浮点数；对整个字符串或者字符串的其中一部分执行操作；对象和浮点数执行自增(increment)或者自减(decrement)；string类型是Redis最基本的数据类型，一个redis中字符串value最多可以是512M。







### Hash（哈希，类似java里的HashMap）

键值对的无序散列表，hash特别适合用于存储对象。
可以添加、获取、移除单个键值对；获取所有键值对

`类似Java里面的Map<String,Object>`




### List（列表）

Redis 列表是简单的字符串列表，`按照插入顺序排序`。你可以添加一个元素导列表的头部（左边）或者尾部（右边）。
`它的底层实际是个链表`

list在可视化界面里就是这个样子
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6c0fcc2c756fc51a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



### Set（集合）

Set是string类型的`无序集合`。它是通过hash表实现实现的，包含字符串的无序收集器(unorderedcollection)，并且被包含的每个字符串都是独一无二的、各不相同；可以添加、获取、移除单个元素；检查一个元素是否存在于某个集合中；计算交集、并集、差集；从集合里卖弄随机获取元素


### Zset(sorted set：有序集合)

 zset 和 set 一样也是string类型元素的集合，且不允许重复的元素。
不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。zset的成员是唯一的,但分数(score)却可以重复。
