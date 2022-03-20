---
title: mybatis-plus-批量插入，先查后插去重问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis-plus-批量插入，先查后插去重问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
如果list本身内部包含了多个重复的行。那么插入时也会去重不成功


; Duplicate entry '202111180182204436' for key 'uni_platform_order_no'; nested exception is java.sql.BatchUpdateException: Duplicate entry '202111180182204436' for key 'uni_platform_order_no'
org.springframework.dao.DuplicateKeyException: com.gbm.cloud.treasure.dao.JgOriginalOrderRepository.insert (batch index #1) failed. Cause: java.sql.BatchUpdateException: Duplicate entry '202111180182204436' for key 'uni_platform_order_no'
; Duplicate entry '202111180182204436' for key 'uni_platform_order_no'; nested exception is java.sql.BatchUpdateException: Duplicate entry '202111180182204436' for key 'uni_platform_order_no'


1、insert 加一个ignore 忽略唯一索引相同的记录，解决其他事务与本事务冲突

2、插入时就对list进行按唯一索引字段去重操作，解决本事务同一个list的元素冲突
~~~
       /**
         * 按platformOrderNo去重excel集合
         */
        dataList = dataList.stream().collect(Collectors.collectingAndThen(Collectors.toCollection(()
                -> new TreeSet<>(Comparator.comparing(JgOriginalOrder::getPlatformOrderNo))), ArrayList::new));
~~~
