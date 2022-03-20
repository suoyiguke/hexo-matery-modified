---
title: 拿到一个sql我们应该从索引上考虑到的优化思考步骤.md
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
title: 拿到一个sql我们应该从索引上考虑到的优化思考步骤.md
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
步骤
step1、 先看join字段，小表驱动大表。大表关联字段上要加索引。若一张表中有2个关联字段那么就要按加载表的顺序设置子索引的顺序。比如 a join b join c ，若先加载c表，那么就要把c.join_colum放在索引的最前面。如：b表上 create index(c.join_colum,a.join_colum)；或者2个索引都建立好，看那种执行计划优秀那就用哪个索引，另一个删除就行。

step2、再看where，最左匹配原则注意下
step3、之后看索引覆盖，尽量做到出现Using index，将其它在select种出现的字段加入到索引的尾巴后面。
step4、其它的DISTINCT、order by、group  by、having 视情况而定
step5、看下设置最佳索引前缀
step6、最后考虑特定大文本类型索引，如url可以做到hash函数转换虚拟列索引或者函数索引、URL翻转建立索引、对JSON类型进行检索的部分加索引
step7、看下各个索引子区分度，高区分度的放前面。调整索引顺序的前提是不影响join和where

小技巧：
1、复杂join查询，select中一定要把不同的表字段放在一起。这样更加直观。对修改索引更加友好
2、创建多种索引组合 index(a,b) index(b,a) mysql会选择其中一个好的方案。因为在join和where种都要复合最左匹配原则！
知道达到最优，然后删除多余的
