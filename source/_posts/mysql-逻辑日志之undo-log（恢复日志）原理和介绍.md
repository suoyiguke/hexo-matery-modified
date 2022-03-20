---
title: mysql-逻辑日志之undo-log（恢复日志）原理和介绍.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-逻辑日志之undo-log（恢复日志）原理和介绍.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
重做日志记录了事务的行为,可以很好地通过其对页进行“重做”操作。但是事务 有时还需要进行回滚操作,这时就需要undo。因此在对数据库进行修改时, InnoDB存 储引擎不但会产生redo,还会产生一定量的undo这样如果用户执行的事务或语句由于某种原因失败了,又或者用户用一条 ROLLBACK语句请求回滚,就可以利用这些undo信息将数据回滚到修改之前的样子。

 redo存放在重做日志文件中,与redo不同,undo存放在数据库内部的一个特殊段 (segment)中,这个段称为undo段(undo segment)undo段位于共享表空间内。可以通过 pyinnodb_pageinfo.py工具来查看当前共享表空间中undo的数量。如下代码显示 当前的共享表空间 ibdatal内有2222个undo页。 "




用户通常对undo有这样的误解:undo用于将数据库物理地恢复到执行语句或事务之前的样子—但事实并非如此。undo是逻辑日志,因此只是将数据库逻辑地恢复到原来的样子。所有修改都被逻辑地取消了,但是数据结构和页本身在回滚之后可能大不相 同。这是因为在多用户并发系统中,可能会有数十、数百甚至数千个并发事务。数据库的主要任务就是协调对数据记录的并发访问比如,一个事务在修改当前一个页中某几条记录,同时还有别的事务在对同一个页中另几条记录进行修改。因此,不能将一个页回滚到事务开始的样子,因为这样会影响其他事务正在进行的工作。

例如,用户执行了一个 INSERT10W条记录的事务,这个事务会导致分配新的 段,即表空间会增大。在用户执行 rollback 时,会将插入的事务进行回滚,但是表空间的大小并不会因此而收缩。因此,当 InnoDB存储引擎回滚时,它实际上做的是与 先前相反的工作。对于每个INSERT, InnoDB存储引擎会完成一个 DELETE;对于每个 DELETE, InnoDB存储引擎会执行一个 INSERT;对于每个 UPDATE, InnoDB存储引 擎会执行一个相反的 UPDATE,将修改前的行放回去。


###undo log 实现了MVCC
除了回滚操作,undo的另一个作用是Mvcc,即在 InnoDB存储引擎中MVCC的 实现是通过undo来完成。当用户读取一行记录时,若该记录已经被其他事务占用,当前事务可以通过undo读取之前的行版本信息,以此实现非锁定读取。

###undo log 会产生redo log
最后也是最为重要的一点是, undo log会产生 redo log,也就是 undo log的产生会伴 随着 redo log的产生,这是因为 undo log也需要持久性的保护。


###undo 存储管理
 InnoDB存储引擎对undo的管理同样采用段的方式。但是这个段和之前介绍的段有所不同。首先 InnoDB存储引擎有 rollback segment,每个回滚段种记录了1024个undo log segment,而在每个 undo log segment段中进行undo页的申请。共享表空间偏移量 为5的页(0,5)记录了所有rollback segment header所在的页,这个页的类型为FL PAGE TYPE SYS. 在 InnoDB11.1版本之前(不包括1.1版本),只有一个 rollback segment,因此支持同 时在线的事务限制为1024。虽然对绝大多数的应用来说都已经够用,但不管怎么说这是 一个瓶颈。从1.1版本开始 InnoDB支持最大128个 rollback segment,故其支持同时在 线的事务限制提高到了128*1024。

虽然 InnoDB11.1版本支持了128个 rollback segment,但是这些 rollback segment都 存储于共享表空间中。 MInnoDB1从1.2版本开始,可通过参数对 rollback segment做进一步 的设置。这些参数包括: 
~~~
SHOW VARIABLES LIKE '%innodb_undo_directory%' 
SHOW VARIABLES LIKE '%innodb_undo_logs%'
SHOW VARIABLES LIKE '%innodb_undo_tablespaces%'
~~~
1、innodb_undo_directory 
 innodb_undo_directory 用于设置 rollback segment文件所在的路径。这意味着 rollback segment可以存放在共享表空间以外的位置,即可以设置为独立表空间。该参数 的默认值为 `.\`,表示当前 InnoDB存储引擎的目录。

2、 innodb_undo_logs
参数 innodb_undo_logs 用来设置 rollback segment的个数,默认值为128.在 InnoDB1.2 版本中,该参数用来替换之前版本的参数 innodb_rollback_segments

3、innodb_undo_tablespaces
参数 innodb_undo_tablespaces 用来设置构成 rollback segment文件的数量,这样 rollback segment可以较为平均地分布在多个文件中。设置该参数后,会在路径 innodb_undo_directory  看到undo为前缀的文件, rol该文件就代表 segment文件图7-13的示例 显示了由3个文件组成的 rollback segment



需要特别注意的是,事务在 undo log segment分配页并写入 undo log的这个过程同样需要写入重做日志。当事务提交时, InnoDB存储引擎会做以下两件事情: 
1、将 undo log 放入列表中,以供之后的 purge操作 
2、判断 undo log 所在的页是否可以重用若可以分配给下个事务使用

事务提交后并不能马上删除 undo log及 undo log所在的页。这是因为可能还有其他 事务需要通过 undo log来得到行记录之前的版本。故事务提交时将 undo log放入一个链表中,是否可以最终删除 undo log及 undo log所在页由 purge线程来判断。


此外,若为每一个事务分配一个单独的undo页会非常浪费存储空间,特别是对于 OLTP 的应用类型。因为在事务提交时,可能并不能马上释放页。假设某应用的删除和更新操作 的TPS( transaction per second)为1000,为每个事务分配一个undo页,那么一分钟就需要 1000*60个页,大约需要的存储空间为1GB。若每秒的 purge页的数量为20,这样的设计对磁盘空间有着相当高的要求。因此,在 InnoDB存储引擎的设计中对undo页可以进行重用（undo 数据被多个事务共享）。 具体来说,当事务提交时,首先将 undo log放入链表中,然后判断undo页的使用空间是否小于3/4,若是则表示该undo页可以被重用,之后新的 undo log记录在当前 undo log的后面。 由于存放 undo log的列表是以记录进行组织的,而undo页可能存放着不同事务 o的 log, 因此 purge操作需要涉及磁盘的离散读取操作是一个比较缓慢的过程。 可以通过命令 SHOW ENGINE INNODB STATUS来查看链表中 undo log的数量,如: 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-19a755292cebcb75.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
