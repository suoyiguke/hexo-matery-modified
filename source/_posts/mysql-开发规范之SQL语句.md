---
title: mysql-开发规范之SQL语句.md
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
title: mysql-开发规范之SQL语句.md
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
1. 【强制】不要使用count(列名)或count(常量)来替代count(*)，count(*)是SQL92定义的标准统计行数的语法，跟数据库无关，跟NULL和非NULL无关。 说明：count(*)会统计值为NULL的行，而count(列名)不会统计此列为NULL值的行。

2. 【强制】count(distinct col) 计算该列除NULL之外的不重复行数，注意 count(distinct col1, col2) 如果其中一列全为NULL，那么即使另一列有不同的值，也返回为0。

3. 【强制】当某一列的值全是NULL时，count(col)的返回结果为0，但sum(col)的返回结果为NULL，因此使用sum()时需注意NPE问题。 正例：使用如下方式来避免sum的NPE问题：SELECT IFNULL(SUM(column), 0) FROM table;

4. 【强制】使用ISNULL()来判断是否为NULL值。 说明：NULL与任何值的直接比较都为NULL。
 1） NULL<>NULL的返回结果是NULL，而不是false。 
 2） NULL=NULL的返回结果是NULL，而不是true。
 3） NULL<>1的返回结果是NULL，而不是true。

5. 【强制】代码中写分页查询逻辑时，若count为0应直接返回，避免执行后面的分页语句。

6. 【强制】不得使用外键与级联，一切外键概念必须在应用层解决。 说明：以学生和成绩的关系为例，学生表中的student_id是主键，那么成绩表中的student_id则为外键。如果更新学生表中的student_id，同时触发成绩表中的student_id更新，即为级联更新。外键与级联更新适用于单机低并发，不适合分布式、高并发集群；级联更新是强阻塞，存在数据库更新风暴的风险；外键影响数据库的插入速度。

7. 【强制】禁止使用存储过程，存储过程难以调试和扩展，更没有移植性。

8. 【强制】数据订正（特别是删除、修改记录操作）时，要先select，避免出现误删除，确认无误才能执行更新语句。

9. 【推荐】in操作能避免则避免，若实在避免不了，需要仔细评估in后边的集合元素数量，控制在1000个之内。

10. 【参考】如果有国际化需要，所有的字符存储与表示，均以utf-8编码，注意字符统计函数的区别。

说明： 
SELECT LENGTH("轻松工作")； 返回为12 
SELECT CHARACTER_LENGTH("轻松工作")； 返回为4 
如果需要存储表情，那么选择utf8mb4来进行存储，注意它与utf-8编码的区别。

11. 【参考】TRUNCATE TABLE 比 DELETE 速度快，且使用的系统和事务日志资源少，但TRUNCATE无事务且不触发trigger，有可能造成事故，故`不建议在开发代码中使用此语句`。
 说明：TRUNCATE TABLE 在功能上与不带 WHERE 子句的 DELETE 语句相同。
