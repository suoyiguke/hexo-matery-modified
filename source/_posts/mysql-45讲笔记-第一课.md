---
title: mysql-45讲笔记-第一课.md
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
title: mysql-45讲笔记-第一课.md
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
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9a0ef7d6fddab74e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###MySQL的框架有几个组件, 各是什么作用?
连接器-->查询缓存--->分析器-->优化器-->执行器--->存储引擎


连接器： 登录权限验证
查询缓存： 命中则直接返回结果
分析器：词法分析、语法分析
优化器：生成执行计划，索引选择
执行器：操作的表有权限验证
存储引擎：存储数据，提供读写接口


###Server层和存储引擎层各是什么作用?
Server层包括连接器、查询缓存、分析器、优化器、执行器等，涵盖MySQL的大多数核心服务功能，以及所有的内置函数（如日期、时间、数学和加密函数等），所有跨存储引擎的功能都在这一层实现，比如存储过程、触发器、视图等。

而存储引擎层负责数据的存储和提取。其架构模式是插件式的，支持InnoDB、MyISAM、Memory等多个存储引擎。现在最常用的存储引擎是InnoDB，它从MySQL 5.5.5版本开始成为了默认存储引擎。




### you have an error in your SQL syntax 这个报错是在词法分析里还是在语法分析里报错?
答案是语法分析


分析器先会做“词法分析”。你输入的是由多个字符串和空格组成的一条SQL语句，MySQL需要识别出里面的字符串分别是什么，代表什么。
MySQL从你输入的"select"这个关键字识别出来，这是一个查询语句。它也要把字符串“T”识别成“表名T”，把字符串“ID”识别成“列ID”。
做完了这些识别以后，就要做“语法分析”。根据词法分析的结果，语法分析器会根据语法规则，判断你输入的这个SQL语句是否满足MySQL语法。
如果你的语句不对，就会收到“You have an error in your SQL syntax”的错误提醒，比如下面这个语句select少打了开头的字母“s”。： “elect”；




###如果表T中没有字段k，而你执行了这个语句 select * from T where k=1, 那肯定是会报“不存在这个列”的错误： “Unknown column ‘k’ in ‘where clause’”。你觉得这个错误是在我们上面提到的哪个阶段报出来的呢？
分析器(语法分析)
>先做词法分析后做语法分析,词法分析主要做的是根据mysql的关键字进行验证和解析，而语法分析会在词法解析的基础上进一步做表名和字段名称的验证和解析；

### 对于表的操作权限验证在哪里进行?
执行器

开始执行的时候，要先判断一下你对这个表T有没有执行查询的权限，如果没有，就会返回没有权限的错误，如下所示(在工程实现上，如果命中查询缓存，会在查询缓存放回结果的时候，做权限验证。查询也会在优化器之前调用precheck验证权限)。

###为什么直到执行器才校验表权限？而不在优化器之前的分析阶段做？
有些时候，SQL语句要操作的表不只是SQL字面上那些。比如如果有个触发器，得在执行器阶段（过程中）才能确定。优化器阶段前是无能为力的


### 执行器的执行查询语句的流程是什么样的?
1、调用InnoDB引擎接口取这个表的第一行，判断ID值是不是10，如果不是则跳过，如果是则将这行存在结果集中；
2、调用引擎接口取“下一行”，重复相同的判断逻辑，直到取到这个表的最后一行。
3、执行器将上述遍历过程中所有满足条件的行组成的记录集作为结果集返回给客户端。

###但是大多数情况下我会建议你不要使用查询缓存，为什么呢？因为查询缓存往往弊大于利。

查询缓存的失效非常频繁，只要有对一个表的更新，这个表上所有的查询缓存都会被清空。因此很可能你费劲地把结果存起来，还没使用呢，就被一个更新全清空了。对于更新压力大的数据库来说，查询缓存的命中率会非常低。除非你的业务就是有一张静态表，很长时间才会更新一次。比如，一个系统配置表，那这张表上的查询才适合使用查询缓存。

好在MySQL也提供了这种“按需使用”的方式。你可以将参数query_cache_type设置成DEMAND，这样对于默认的SQL语句都不使用查询缓存。而对于你确定要使用查询缓存的语句，可以用SQL_CACHE显式指定，像下面这个语句一样：
mysql> select SQL_CACHE * from T where ID=10；
需要注意的是，MySQL 8.0版本直接将查询缓存的整块功能删掉了，也就是说8.0开始彻底没有这个功能了。
query_cache_size 参数虽然不用了,我想确认下,关闭情况是 query_cache_size=0 要匹配参数query_cache_type=off吗？ 还是直接query_cache_size=0 即可？
这两个都可以，不过用query_cache_type会好些（代码判断路径更短）


###wait_timeout 和interactive_timeout设置问题
wait_timeout 是客户端 非交互式的连接时间，如果程序连接mysql SERVER，是交互连接,关联的时间参数为interactive_timeout, 这两个时间参数需要尽量一致吗,一般设置多少合适?
是的，这两个尽量设置成相同。值的话取决于业务。如果你面对的是成熟的开发（比如公司内部团队），可以设置小些，分钟级别就行。
>这两个参数设置太长 8小时容易导致维护的连接过多，占用内存过大

数据库里面，长连接是指连接成功后，如果客户端持续有请求，则一直使用同一个连接。短连接则是指每次执行完很少的几次查询就断开连接，下次查询再重新建立一个。
**建立连接的过程通常是比较复杂的，所以我建议你在使用中要尽量减少建立连接的动作，也就是尽量使用长连接。**但是全部使用长连接后，你可能会发现，有些时候MySQL占用内存涨得特别快，这是因为MySQL在执行过程中临时使用的内存是管理在连接对象里面的。这些资源会在连接断开的时候才释放。所以如果长连接累积下来，可能导致内存占用太大，被系统强行杀掉（OOM），从现象看就是MySQL异常重启了。
怎么解决这个问题呢？你可以考虑以下两种方案。

1、定期断开长连接。使用一段时间，或者程序里面判断执行过一个占用内存的大查询后，断开连接，之后要查询再重连。

2、如果你用的是MySQL 5.7或更新版本，可以在每次执行一个比较大的操作后，通过执行 mysql_reset_connection来重新初始化连接资源。这个过程不需要重连和重新做权限验证，但是会将连接恢复到刚刚创建完时的状态。
