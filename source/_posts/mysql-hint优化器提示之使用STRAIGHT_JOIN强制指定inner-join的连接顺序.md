---
title: mysql-hint优化器提示之使用STRAIGHT_JOIN强制指定inner-join的连接顺序.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-hint优化器提示之使用STRAIGHT_JOIN强制指定inner-join的连接顺序.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
用explain进行分析，发现执行顺序为Table1->Table2，这时就由Table1来作为驱动表了，Table1中相应的索引也就用上了，执行时间竟然低于1s了。

分析到这里，必须要重点说下：

STRAIGHT_JOIN只适用于inner join，并不使用与left join，right join。（因为left join，right join已经代表指定了表的执行顺序）
尽可能让优化器去判断，因为大部分情况下mysql优化器是比人要聪明的。使用STRAIGHT_JOIN一定要慎重，因为啊部分情况下认为指定的执行顺序并不一定会比优化引擎要靠谱。
 
~~~
但如下sql的执行时间都少于1s：

select t1.*
from Table1 t1
where t1.FilterID = 1
或

select t1.*
from Table1 t1
inner join Table2 t2
on t1.CommonID = t2.CommonID
 这个时候STRAIGHT_JOIN就派上用场，我们对sql进行改造如下：

select t1.*
from Table1 t1
STRAIGHT_JOIN  Table2 t2
on t1.CommonID = t2.CommonID
where t1.FilterID = 1
~~~
