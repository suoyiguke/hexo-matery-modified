---
title: mysql-开发规范之ORM映射.md
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
title: mysql-开发规范之ORM映射.md
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
1. 【强制】在表查询中，`一律不要使用 * 作为查询的字段列表，需要哪些字段必须明确写明`。 说明：1）增加查询分析器解析成本。2）增减字段容易与resultMap配置不一致。3）无用字段增加网络消耗，尤其是text类型的字段。

2. 【强制】POJO类的布尔属性不能加is，而数据库字段必须加is_，要求在resultMap中进行字段与属性之间的映射。 说明：参见定义POJO类以及数据库字段定义规定，在<resultMap>中增加映射，是必须的。在MyBatis Generator生成的代码中，需要进行对应的修改。

3. 【强制】不要用resultClass当返回参数，即使所有类属性名与数据库字段一一对应，也需要定义；反过来，每一个表也必然有一个POJO类与之对应。 说明：配置映射关系，使字段与DO类解耦，方便维护。

4. 【强制】sql.xml配置参数使用：#{}，#param# 不要使用${} 此种方式容易出现SQL注入。

5. 【强制】iBATIS自带的queryForList(String statementName,int start,int size)不推荐使用。 说明：其实现方式是在数据库取到statementName对应的SQL语句的所有记录，再通过subList取start,size的子集合。
正例：Map<String, Object> map = new HashMap<>();
map.put("start", start);
map.put("size", size);


6. 【强制】不允许直接拿HashMap与Hashtable作为查询结果集的输出。 说明：resultClass=”Hashtable”，会置入字段名和属性值，但是值的数据类型不可控。

7. 【强制】更新数据表记录时，必须同时更新记录对应的gmt_modified字段值为当前时间。

8. 【推荐】不要写一个大而全的数据更新接口。传入为POJO类，不管是不是自己的目标更新字段，都进行update table set c1=value1,c2=value2,c3=value3; 这是不对的。执行SQL时，不要更新无改动的字段，一是易出错；二是效率低；三是增加binlog存储。


9. 【参考】@Transactional事务不要滥用。事务会影响数据库的QPS，另外使用事务的地方需要考虑各方面的回滚方案，包括缓存回滚、搜索引擎回滚、消息补偿、统计修正等。

>所以只是查询的上方法上不要加 @Transactional，避免无谓增加 QPS


10. 【参考】<isEqual>中的compareValue是与属性值对比的常量，一般是数字，表示相等时带上此条件；<isNotEmpty>表示不为空且不为null时执行；<isNotNull>表示不为null值时执行。
