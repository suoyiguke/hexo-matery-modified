---
title: mysql--sql预处理-Prepared-Statements.md
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
title: mysql--sql预处理-Prepared-Statements.md
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
###使用sql预编译的优势
1、使用PAREPARE STATEMENT可以减少每次执行SQL的语法分析，比如用于执行带有WHERE条件的SELECT和DELETE，或者UPDATE，或者INSERT，只需要每次修改变量值即可。这样有些性能上的帮助。

2、同样可以防止SQL注入，参数值可以包含转义符和定界符。

3、使用在应用程序中，比如我们java JDBC的`PreparedStatement` 可以达到类似的预编译效果，可以看看这篇
https://www.jianshu.com/p/19a9f2340ebe 。
当然也可以使用sql脚本来完成。


###使用PREPARE 来预编译一条sql

1、语句的名字不区分大小写。准备好的SQL语句名字可以是字符串，也可以是用户指定的包含SQL文本的变量。
2、PREPARE中的SQL文本必须代表一条单独的SQL语句而不能是多条SQL语句。
3、在SQL语句中，? 字符用来作为后面执行查询使用的一个参数。? 不能加上引号，及时打算将它们绑定到字符变量中也不可以。

###使用EXECUTE .. USING .. 来执行sql

使用PREPARE准备语句后，可以使用引用准备好的语句名称。如果准备好的语句包含任何`参数标记`，则必须提供USING子句，该子句列出包含要绑定到参数的值的`用户变量`。`参数值只能由用户变量提供`，USING子句的名称必须与多个变量作为语句中的参数标记数。

>可以多次使用EXECUTE 执行给定的prepared语句，向其传递不同的变量或设置在每次执行之前将变量设置为不同的值。


###请使用DEALLOCATE PREPARE语句释放资源

每一次执行完EXECUTE时，养成好习惯，须执行DEALLOCATE PREPARE … 语句，这样可以释放执行中使用的所有数据库资源（如游标）。

不仅如此，如果一个session的预处理语句过多，可能会达到max_prepared_stmt_count的上限值。



###预处理的限制
预处理语句只能在创建者的`当前会话`中可以使用，其他会话是无法使用的。
而且在任意方式（正常或非正常）退出会话时，之前定义好的预处理语句将不复存在。
如果在存储过程中使用，如果不在过程中DEALLOCATE掉，在存储过程结束之后，该预处理语句仍然会有效。


###举个例子

1、使用预编译来完成分页sql查询
~~~
# 预编译sql，使用 ? 进行参数绑定
PREPARE getList  FROM 'SELECT * FROM tb_box WHERE id > ? LIMIT ?';
# 执行
SET  @id:=10000,@pagesize:=20;
EXECUTE getList  USING @id,@pagesize;
# 解绑
DEALLOCATE PREPARE getList;
~~~

2、可以使用预处理的方式在limit中使用用户变量
~~~
SET @ps:= 10;
PREPARE s1 FROM 'SELECT *  FROM box_fenqu ORDER BY create_time DESC LIMIT ?';
EXECUTE s1 USING @ps;
DEALLOCATE PREPARE s1;
~~~
