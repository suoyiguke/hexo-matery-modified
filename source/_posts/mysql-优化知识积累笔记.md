---
title: mysql-优化知识积累笔记.md
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
title: mysql-优化知识积累笔记.md
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
###数据库优化方向总结
####设计方向
- 字段设计。尽量使用小范围。如11位手机号就使用char(11)
- 避免join过多表，可以采用反范式化的设计
- ip字段我们可以使用 mysql函数iprr()将ipv4它转为数值类型存储
####索引方向
- 什么时候要建立索引。建立的时候，像一些记录比较少的。只有成百上签行。那么久不需要；字段的重复率高。有个公式：去重后的字段/全部字段数 越接近100%那么就是越可以建立索引的。比如像男女这样枚举的字段就不建议建立索引。因为建立后效率也不高。

- 怎么建立索引，最好建立的是联合索引
- 索引最左匹配原则
- 索引什么时候会失效
- explaint

####sql写法上
- 像一些where条件非常多、join表也多。可以试下只查 id出来。然后再用id去查额外的信息。延迟查询的思想
- OR 条件会导致索引失效。所以我们可以将它改写为UNION ALL 语句或者使用IN来代替
- 

####业务方向
- 分页查询优化。设计时可以取消这个总页数、总记录数的查询。取消跳页查询。只留下上一页或下一页
- 根据业务调整索引结构。

####数据库本身的参数
- 首当其冲的就是 innodb_buffer_pool_size 
- join_buffer_size
- sort_buffer_size
- tmp_table_size 
- innodb_thread_concurrency 默认是0

###sql写法上
1、禁用 select * ，用具体的字段列表代替 *，不要返回用不到的任何字段。

2、实现随机排序请不要用order by rand()
它的逻辑就是随机排序（为每条数据生成一个随机数，然后根据随机数大小进行排序）。如select * from student order by rand() limit 5的执行效率就很低，因为它为表中的每条数据都生成随机数并进行排序，而我们只要前5条。
解决思路：在应用程序中，将随机的主键生成好，去数据库中利用主键检索。

3、查询单条记录时使用limit 1
如果可以确定仅仅检索一条，建议加上`limit 1`，其实ORM框架帮我们做到了这一点（查询单条的操作都会自动加上`limit 1`）。

4、对于判断是否存在具体记录，推荐使用limit 1而不是count。让数据库查询时遇到一条就返回，不要再继续查找还有多少条了，业务代码中直接判断是否非空即可.
SQL写法:SELECT 1 FROM table WHERE a = 1 AND b = 2 LIMIT 1

5、用 PreparedStatement， 一般来说比 Statement 性能高，一个 sql发给服务器去执行，涉及步骤：语法检查、语义分析， 编译，缓存。

7、OR可以改写成IN，OR的效率是n级别，IN的效率是log(n)级别，in的个数建议控制在200以内。
EXPLAIN SELECT * FROM book where id =1 OR id=100 改写为
EXPLAIN SELECT * FROM book where id in (1,100)

8、OR 还可以改写为 UNION ALL，当OR的两边条件作用不同字段时就可以这样做！

 EXPLAIN SELECT * FROM book where id =1 UNION ALL SELECT * FROM book where gg =100


9、in 和 not in 也要慎用，否则会导致全表扫描，如：select id from t where num in(1,2,3) 对于连续的数值，能用 between 就不要用 in 了：select id from t where num between 1 and 3


10、在所有的存储过程和触发器的开始处设置 SET NOCOUNT ON ，在结束时设置 SET NOCOUNT OFF 。无需在执行存储过程和触发器的每个语句后向客户端发送DONE_IN_PROC 消息。

11、尽量不要使用子查询，有些子查询可以使用 join using(id) 来改写
12、有时可以考虑使用`延迟加载`的思想。先将id查出来，然后去根据id查
13、批量插入，使用 INSERT INTO tb values(),(),()..() 的形式。因为insert语句合并后日志量的binlog和innodb的事务让日志）减少了，降低日志刷盘的数据量和频率，从而提高效率。通过合并SQL语句，同时也能减少SQL语句解析的次数，减少网络传输的IO。`注意`SQL语句是有长度限制，在进行数据合并在同一SQL中务必不能超过SQL长度限制，通过max_allowed_packet配置可以修改，默认是1M，测试时修改为8M。

14、批量插入，尽量选择数值类型的主键有序的递增插入


15、`小表驱动大表` in和EXISTS 两种方式数据会是样的，但是性能不一定。需要自己测试

使用in
SELECT * FROM tb1_emp e WHERE e.deptId in (SELECT id FROM tb1_dept d);

使用EXISTS  SELECT * FROM tb1_emp e WHERE EXISTS (SELECT id FROM tb1_dept d WHERE e.deptId = d.id);


16、最大值和最小值优化，使用 ORDER BY LIMIT 1 来代替函数

问题sql：SELECT MIN(id) FROM logs1 WHERE logurl = '/index'
优化方式：SELECT id FROM logs1 WHERE logurl = '/index' ORDER BY id LIMIT 1

17、order by，gruop by 优化
https://www.jianshu.com/p/8bd0ddc26974

18、join 优化
https://www.jianshu.com/p/f08c0bde07db

19、count 优化
https://www.jianshu.com/p/240efe0570e9

20、分页优化
https://www.jianshu.com/p/b4eb74b76f79

21、优化UNION
UNION语句默认是移除重复记录的，需要用到排序操作，如果结果集很大，成本将会很高，所以，建议尽量使用UNION ALL语句。对于UNION多个分表的场景，应尽可能地在数据库分表的时候，就确定各个分表的数据是唯一的，这样就无须使用 UNION来去除重复的记录了。

 另外，查询语句外层的WHERE条件，并不会应用到每个单独的UNION子句内，所以，应在每一个UNION子句中添加上 WHERE条件，从而尽可能地限制检索的记录数

22、不要使用SQL_CALC_FOUND_ROWS，请用count(*)代替之

23、 优化 Using temporary
https://www.jianshu.com/p/56dabc67198e

24、优化filesort
https://www.jianshu.com/p/7cf41245a015

###表设计、字段设计上

1、尽可能使用 not null，非null字段的处理要比null字段的处理高效些！且不需要判断是否为null。比如 is null 使用在where条件中会导致索引失效，进而影响查询sql的执行效率。null在MySQL中，不好处理，存储需要额外空间，运算也需要特殊的运算符。如select null = null和select null <> null（<>为不等号）有着同样的结果，只能通过is null和is not null来判断字段是否为null。尽量使用默认值来代替null；因此通常使用特殊的数据进行占位，比如int not null default 0、string not null default ‘’

2、单表字段不宜过多，二三十个就极限了,一定需要那么多字段就可以使用垂直分表。主键尽量设置为数值类型int，并设置为 AUTO_INCREMENT自增。不要在程序中自己设置主键值

3、字段注释要完整，见名知意

4、数值类型尽量使用无符号。对于业务上不考虑负数的情况下尽量使用无符号 `UNSIGNED` 修饰。这样可以在不增加存储消耗的情况下增大存储数据范围

5、尽量使用数字型字段，若只含数值信息的字段尽量不要设计为字符型，这会降低查询和连接的性能，并会增加存储开销。这是因为引擎在处理查询和连接时会逐个比较字符串中每一个字符，而对于数字型而言只需要比较一次就够了。


6、 有外键约束会影响插入和删除性能，如果程序能够保证数据的完整性，那在设计数据库时就去掉外键。


7、对于一些常用业务字段的字段类型设计；注意可以应用`前缀索引`、`虚拟列`等技术使索引起最大的作用
https://www.jianshu.com/p/93d91f5192a0


8、适当使用冗余数据`反范式化设计`
有时最好的办法是在表中保存冗余的数据，虽然这些冗余数据有时也可以由其他的列推断得出。冗余数据可以让查询执行 得更快。比如，我们可以增加一个专门的计数表或计数字段，实时更新计数信息。比如，大表之间的连接操作很耗时，增加冗余字段则可以有效地减少连接的表的个数，这样就避免了多表的join

9、计算复用，使用缓存表
我们可以使用缓存表存储一些结果，这里所说的“缓存表”，意思是这些值在逻辑上是冗余的，可以从原始表中获取到，但 显然从原始表中获取数据更慢

10、预计算

预先对一些常用的大查询生成汇总表。我们需要有这样一个意识，如果你需要处理大量数据，一般需要昂贵的计算成本。 所以预计算往往是值得考虑的好方法。我们可以把查询结果存储到独立的汇总表中，或者可以把相关联的表的一些字段存放在 一个独立的新表中，基于这个新的汇总表去做统计。 当我们使用缓存表和汇总表时，我们要做出决定：是实时更新数据还是定期更新，这依赖于你的应用。 当我们实时或定期重建缓存表、汇总表的时候，我们需要数据在操作的时间范围内仍然可用。我们可以采用一种“影子 表”的方法，即建立一个临时表，在建立好之后，通过原子性地重命名表的操作，实现切换。



###索引上
1、应尽量避免在 where 子句中对字段进行 null 值判断，否则将导致引擎放弃使用索引而进行全表扫描，如：select id from t where num is null可以在num上设置默认值0，确保表中num列没有null值，然后这样查询：select id from t where num=0


2、应尽量避免在 where 子句中使用!=或<>操作符，否则引擎将放弃使用索引而进行全表扫描。


3、应尽量避免在 where 子句中使用or 来连接条件，否则将导致引擎放弃使用索引而进行全表扫描，如：select id from t where num=10 or num=20可以使用 union all来代替or：select id from t where num=10 union all select id from t where num=20




4、如果在 where 子句中使用参数，也会导致全表扫描。因为SQL只有在运行时才会解析局部变量，但优化程序不能将访问计划的选择推迟到运行时；它必须在编译时进行选择。然 而，如果在编译时建立访问计划，变量的值还是未知的，因而无法作为索引选择的输入项。如下面语句将进行全表扫描：select id from t where num=@num可以改为强制查询使用索引：select id from t with(index(索引名)) where num=@num

5、应尽量避免在 where 子句中对字段进行表达式操作，这将导致引擎放弃使用索引而进行全表扫描。如：select id from t where num/2=100应改为:select id from t where num=100*2



6、应尽量避免在where子句中对字段进行函数操作，这将导致引擎放弃使用索引而进行全表扫描。如：select id from t where substring(name,1,3)=’abc’ ，name以abc开头的id应改为:
select id from t where name like ‘abc%’

7、注意索引的`最左匹配原则`。在使用索引字段作为条件时，如果该索引是复合索引，那么必须使用到该索引中的第一个字段作为条件时才能保证系统使用该索引，否则该索引将不会被使用，并且应尽可能的让字段顺序与索引顺序相一致。

8、并不是所有索引对查询都有效，SQL是根据表中数据来进行查询优化的，当索引列有大量数据重复时，SQL查询可能不会去利用索引，如一表中有字段sex，male、female几乎各一半，那么即使在sex上建了索引也对查询效率起不了作用。

9、索引并不是越多越好，索引固然可以提高相应的 select 的效率，但同时也降低了 insert 及 update 的效率，因为 insert 或 update 时有可能会重建索引，所以怎样建索引需要慎重考虑，视具体情况而定。一个表的索引数最好不要超过6个，若太多则应考虑一些不常使用到的列上建的索引是否有必要。

10、在varchar这样字符类型上建立索引时，可以使用`前缀索引`的思想，只给前几个字符建立索引。不过要确保节省空间的同时索引的效率要达到。

11、多表join添加索引时，需要在关联字段上加索引。左连接加右表，右连接加左表（其实就是加内部表上）。不需要两边都加

12、where条件中有多个列条件。请使用复合索引，而不是为每个单独的列创建单值索引单值索引。因为单值索引只有一个会生效，造成空间浪费

13、可以定时的去修复索引碎片提高查询效率
https://www.jianshu.com/p/4272923ae89b

14、
