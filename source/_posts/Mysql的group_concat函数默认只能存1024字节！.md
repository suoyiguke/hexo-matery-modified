---
title: Mysql的group_concat函数默认只能存1024字节！.md
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
title: Mysql的group_concat函数默认只能存1024字节！.md
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
Mysql的group_concat函数默认只能存1024字节！


今天在一个场景中使用到了mysql的group_concat函数，按以往的实践经历数据量很小的时候很难发现问题所在，然后今天在group_concat大数据量的时候发现了问题，打印出来显示读取出来的数据只有1024个字节！度娘了下，发现可以通过在mysql的配置文件中增加配置：group_concat_max_len = 102400 #你要的最大长度  来解决暂时的问题。但我不推荐这么做，因为如果哪天数据量超出了这个范围导致出现读取数据不全的问题，后果是不堪设想的，所以我推荐还是得在业务逻辑代码中去进行相应的修改，比如在业务代码中自己拼接。

~~~
set GLOBAL group_concat_max_len = 102400
set session group_concat_max_len = 102400

show VARIABLES like '%group_concat_max_len%'
~~~

