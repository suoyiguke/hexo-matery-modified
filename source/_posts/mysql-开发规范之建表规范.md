---
title: mysql-开发规范之建表规范.md
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
title: mysql-开发规范之建表规范.md
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
###建表规范

1、【强制】表达是与否概念的字段，必须使用is_xxx的方式命名，数据类型是unsigned tinyint（1表示是，0表示否）。 说明：任何字段如果为非负数，必须是unsigned。 注意：POJO类中的任何布尔类型的变量，都不要加is前缀，所以，需要在<resultMap>设置从is_xxx到Xxx的映射关系。数据库表示是与否的值，使用tinyint类型，坚持is_xxx的命名方式是为了明确其取值含义与取值范围。 正例：表达逻辑删除的字段名is_deleted，1表示删除，0表示未删除。

2、【强制】表名、字段名必须使用小写字母或数字，禁止出现数字开头，禁止两个下划线中间只出现数字。数据库字段名的修改代价很大，因为无法进行预发布，所以字段名称需要慎重考虑。 说明：MySQL在Windows下不区分大小写，但在Linux下默认是区分大小写。因此，数据库名、表名、字段名，都不允许出现任何大写字母，避免节外生枝。 正例：aliyun_admin，rdc_config，level3_name 反例：AliyunAdmin，rdcConfig，level_3_name

3、【强制】表名不使用复数名词。 说明：表名应该仅仅表示表里面的实体内容，不应该表示实体数量，对应于DO类名也是单数形式，符合表达习惯。



4. 【强制】禁用保留字，如desc、range、match、delayed等，请参考MySQL官方保留字。

5. 【强制】主键索引名为pk_字段名；唯一索引名为uk_字段名；普通索引名则为idx_字段名。 说明：pk_ 即primary key；uk_ 即 unique key；idx_ 即index的简称。

6. 【强制】小数类型为decimal，禁止使用float和double。 说明：在存储的时候，float 和 double 都存在精度损失的问题，很可能在比较值的时候，得到不正确的结果。如果存储的数据范围超过 decimal 的范围，建议将数据拆成整数和小数并分开存储。



7. 【强制】如果存储的字符串长度几乎相等，使用char定长字符串类型。

8. 【强制】varchar是可变长字符串，不预先分配存储空间，长度不要超过5000，如果存储长度大于此值，定义字段类型为text，独立出来一张表，用主键来对应，避免影响其它字段索引效率。



9. 【强制】表必备三字段：id, create_time, update_time。 说明：其中id必为主键，类型为bigint unsigned、单表时自增、步长为1。create_time, update_time的类型均为datetime类型。


10. 【推荐】表的命名最好是遵循“业务名称_表的作用”。 正例：alipay_task / force_project / trade_config
11. 【推荐】库名与应用名称尽量一致。
12. 【推荐】如果修改字段含义或对字段表示的状态追加时，需要及时更新字段注释。

13. 【推荐】字段允许适当冗余，以提高查询性能，但必须考虑数据一致。冗余字段应遵循：
 1） 不是频繁修改的字段。 2） 不是varchar超长字段，更不能是text字段。3） 不是唯一索引的字段。 正例：商品类目名称使用频率高，字段长度短，名称基本一不变，可在相关联的表中冗余存储类目名 称，避免关联查询。


14. 【推荐】单表行数超过500万行或者单表容量超过2GB，才推荐进行分库分表。 说明：如果预计三年后的数据量根本达不到这个级别，请不要在创建表时就分库分表。

15. 【参考】合适的字符存储长度，不但节约数据库表空间、节约索引存储，更重要的是提升检索速度。 正例：如下表，其中无符号值可以避免误存负数，且扩大了表示范围。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f02560aa723148a0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
