---
title: mysql-参数调优（12）之innodb_thread_concurrency、innodb_concurrency_tickets-合理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-参数调优（12）之innodb_thread_concurrency、innodb_concurrency_tickets-合理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
>设置这个参数在mysql低负载时没有效果，建议在mysql非常繁忙时可以关注并配置


你可能会经常听到应该设置 innodb_thread_concurrency=0 （表示不进行并发线程数量控制）然后就不要管它了。不过这个只在低负载服务器使用时才正确。然后，如果你的服务器的CPU或者IO使用接受饱和，特别是偶尔出现峰值，这时候系统想在超载时能正常处理查询，那么强烈建议关注 innodb_thread_concurrency。
InnoDB有一种方法来控制并行执行的线程数： 我们称为`并发控制机制`。大部分是由 innodb_thread_concurrency 值来控制的。如果设置为0，并发控制就关闭了，因此InnoDB会立即处理所有进来的请求(尽可能多的)。

在你有32CPU核心且只有4个请求时会没什么问题(CPU低负载)。不过想像下你只有4CPU核心和32个请求时(CPU高负载) ， 如果你让32个请求同时处理，就会有大量的线程属于block争用锁状态，可能出现大量的线程上下文切换（这对cpu资源是一种不必要的消耗），因为这些32个请求只有4 CPU核心，显然地会比平常慢至少8倍(实际上是大于8倍)，而然这些请求每个都有自己的外部和内部锁，这有很大可能堆积请求。若此时将 innodb_thread_concurrency 设置为4，那么没有争用到锁的其它24个请求都会进入到waitting队列(FIFO先进先出)，而处于waitting状态的请求是不会去争用对象锁的，这样就不需要去进行mysql内部线程之间的上下文切换，高效的利用CPU性能。
>进行上文切换还不如把线程处于睡眠态放弃CPU使用权。让CPU集中精力去处理业务而不是分心去做其它事情


**使用以下指南来帮助查找和维护适当的设置**

对于大多数工作负载和服务器，设置为8（cpu线程数）是一个好开端，然后你可以根据服务器达到了这个限制而资源使用率利用不足时逐渐增加。

可以通过 show engine innodb status 来查看目前查询处理情况，查找类似如下行：22 queries inside InnoDB, 104 queries in queue。这表示22个查询被innodb处理，104个查询进入wait queue 队列。若此mysql部署在8核心的机器上，意味着有22个线程在争用8个核心。queries inside InnoDB的数量特别大得话就要考虑降低 innodb_thread_concurrency 的值了；如果设置为0后show engine status的下面值始终为0：0 queries inside InnoDB, 0 queries in queue





**推荐设置**
推荐设置：  装mysql的服务器的cpu的核数，64核cpu 那么推荐：64（<=cpu核数） 

寻找最合适的值：如果一个工作负载中，并发用户线程的数量小于等于64，建议设置innodb_thread_concurrency=0;而事实上我们的系统是处于大并发大事务的情况下的，怎么来算这个值？建议是先设置为128，然后我们不断的降这个值，直到发现能够提供最佳性能的线程数。为了安全起间我们会把它设成和cpu核心线程数一样大小。 
如果不配的后果：  默认在64位下会是8  配置实例：  innodb_thread_concurrency = 64

innodb_thread_concurrency是一个动态变量，它允许在一个实时测试系统上试验不同的设置。如果某个特定设置的性能很差，可以快速将innodb_thread_concurrency设置回0。

~~~
SET global innodb_thread_concurrency = 0;
~~~




**为了更好的理解innodb_thread_concurrency我们可以做下实验**

我将同一时刻能够进入innodb干活的线程数设置了1，同时tickets设置为了10来尽可能的观察到这种不断进入innodb层次，然后tickets到被提出innodb层次的现象，随后我做了2个大事务

~~~
SET GLOBAL innodb_thread_concurrency = 1;
SET GLOBAL innodb_concurrency_tickets = 10;
~~~



然后执行show engine innodb status，得到以下信息：
~~~
--------------
ROW OPERATIONS
--------------
1 queries inside InnoDB, 1 queries in queue
2 read views open inside InnoDB
Process ID=5204, Main thread ID=5596, state: sleeping
Number of rows inserted 2100165, updated 1, deleted 0, read 2729033
28092.76 inserts/s, 0.00 updates/s, 0.00 deletes/s, 28092.71 reads/s
----------------------------
END OF INNODB MONITOR OUTPUT
~~~
`1 queries inside InnoDB, 1 queries in queue` 这里也明显的说了1个线程在innodb里面另外一个在等待队列；


然后快速执行多次查询当前的活跃事务 
~~~
mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx;
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| trx_id   | trx_state | trx_query                                 | trx_operation_state             | trx_concurrency_tickets |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| 14022294 | RUNNING   | NULL                                      | NULL                            |                       0 |
| 14022289 | RUNNING   | INSERT into book_1 SELECT * from book_old | fetching rows                   |                       3 |
| 14022284 | RUNNING   | INSERT into book_2 SELECT * from book_old | sleeping before entering InnoDB |                       0 |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
3 rows in set (0.03 sec)

mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx;
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| trx_id   | trx_state | trx_query                                 | trx_operation_state             | trx_concurrency_tickets |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| 14022289 | RUNNING   | INSERT into book_1 SELECT * from book_old | sleeping before entering InnoDB |                       0 |
| 14022284 | RUNNING   | INSERT into book_2 SELECT * from book_old | inserting                       |                       7 |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
2 rows in set (0.03 sec)

mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx;
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| trx_id   | trx_state | trx_query                                 | trx_operation_state             | trx_concurrency_tickets |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| 14022289 | RUNNING   | INSERT into book_1 SELECT * from book_old | inserting                       |                       8 |
| 14022284 | RUNNING   | INSERT into book_2 SELECT * from book_old | sleeping before entering InnoDB |                       0 |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
2 rows in set (0.03 sec)

mysql> select trx_id,trx_state,trx_query,trx_operation_state,trx_concurrency_tickets from information_schema.innodb_trx;
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| trx_id   | trx_state | trx_query                                 | trx_operation_state             | trx_concurrency_tickets |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
| 14022289 | RUNNING   | INSERT into book_1 SELECT * from book_old | inserting                       |                       6 |
| 14022284 | RUNNING   | INSERT into book_2 SELECT * from book_old | sleeping before entering InnoDB |                       0 |
+----------+-----------+-------------------------------------------+---------------------------------+-------------------------+
2 rows in set (0.04 sec)
~~~

可以看到这两个大事务的 trx_opreation_state 字段值在 `sleeping before entering InnoDB`和`inserting`之间交替变换。他们不断的在进行`轮换交替的进入的innodb层次`，同时我们还能看到活跃事务trx_concurrency_tickets这个tickets不断的减少，而处于sleeping before entering InnoDB的事务其trx_concurrency_tickets为0。

>处于inserting下的线程的trx_concurrency_tickets值会随时间递减，等到为0时就会让出cpu执时间片，相应的状态变为 sleeping before entering InnoDB



**innodb的线程并发相关参数**
好了有了上面的理论知识可以进行这几个参数的解释了其实这三个参数就是来解决上面的问题
1、innodb_thread_concurrency
同一时刻能够进入innodb层次并发执行的线程数(注意是并发不是并行)，如果超过CPU核数，某些线程可能处于就绪态而没有获得CPU时间轮片，如果SERVER层的线程大于这个值，那对不起，多余的线程将会被放到一个叫做wait queue的队列中，而不能进入INNODB层次，进不到innodb层当然也就不能干活了，谈不上获得CPU。既然是一个队列那么它必然满足先进入先出的原则。这也是前面说的长痛不如短痛，与其让你不断的进行上文切换还不如把你处于睡眠态放弃CPU使用权，默认这个值是0，代表不限制。
2、innodb_concurrency_tickets
这个参数设置为一种tickets,默认是5000，我也不清楚到底它代表多久，从官方文档来看它和事物处理的行数有关，大事物需要处理的行数自然更多，小事物当然也就越少至少 `我们可以想成获得CPU的时间`，干活期间他会不断减少，如果减少到0，这个线程将被提出innodb层次，进入前面说的等待队列，当然也就在队尾部了，这里假设有一个小的事物正在排队进入innodb层，又或者它已经进入了innodb层没有获得CPU时间轮片，突然一个大的事物tickets耗尽被提出了innodb层，那么这个小事物就自然而然能够获得CPU轮片干活，而小事物执行非常快，执行完成后另外的事物又能尽快的获得CPU干活，不会由于OS线程调度不均匀的问题而造成的小事物饥饿问题，这很好理解。也就是前面我说的与其依赖OS的调度策略不如自己设置一种规则，让用到了一定时间轮片的线程先处于睡眠态放弃CPU的使用。
3、innodb_thread_sleep_delay
这个参数从官方手册来看，是代表当`事物被踢出innodb层次后自己睡眠的时间`，等待睡眠完成后再次进入wait que队列5.6.3以后可以设置innodb_adaptive_max_sleep_delay，来自动调整innodb_thread_sleep_delay，这就更为方便，因为这个值很难讲多少合适，其单位是microseconds，从某种意义上来讲这个值加剧了大事物执行的时间，小事物也就更加容易进入INNODB层次获得CPU时间来干活。

关于这几个值如果一旦innodb_thread_concurrency设置为0，其他值的设置均没有效果，这很好理解，设置为0后表示不限制，如果不限制也就谈不上等待队列，没有等待队列睡眠多久进入等待队列自然没有意义。如果设置为0后show engine status的下面值始终为0;
0 queries inside InnoDB, 0 queries in queue

