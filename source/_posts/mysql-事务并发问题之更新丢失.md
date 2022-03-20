---
title: mysql-事务并发问题之更新丢失.md
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
title: mysql-事务并发问题之更新丢失.md
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

>两个事务同时操作相同的数据，后提交的事务会覆盖先提交的事务处理结果


使用银行转账的经典例子来帮助理解，这里的更新丢失是因为`并发读后写`造成的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0cb09a25dbe772ba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###更新丢失模拟

**mysql数据准备**
~~~


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb
-- ----------------------------
DROP TABLE IF EXISTS `tb`;
CREATE TABLE `tb`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `yk` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb
-- ----------------------------
INSERT INTO `tb` VALUES (1, 0);

SET FOREIGN_KEY_CHECKS = 1;

~~~

**使用python操作mysql**
做这种简单操作使用python的sqlalchemy比较方便，java的jdbc的话也行~
- 使用线程A和线程B，分别对tb表字段yk进行叠加
- 线程A叠加100次，线程B叠加150次，最终结果应该是250次
- 线程A和线程B在这里我也称作为事务A和事务B帮助理解
~~~
import threading
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(user='root', password='yk123',
                                                                        host='localhost',
                                                                        port='3306',
                                                                        database='test'),
    max_overflow=int(1),  # 超过连接池大小外最多创建的连接
    pool_size=int(5),  # 连接池大小,默认是5
    pool_timeout=int(1),  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=int(0)  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)



# 修改
def add(count):
    for i in list(range(1,count)):
        print(threading.currentThread().getName()+"==>"+str(i))
        connection = engine.connect(close_with_result=False)
        trans = connection.begin()
        ex = connection.execute("SELECT yk FROM tb WHERE id = %(id)s;", id=1)
        y = ex.first()
        yk = y[0]
        yk = yk + 1
        connection.execute("UPDATE tb SET yk =  %(yk)s WHERE id = 1;",yk=yk)
        trans.commit()


# 测试
if __name__ == '__main__':
    # 用线程去执行函数
    t1 = Thread(target=add,args=(101,)) # 100次
    t1.setName("线程A")

    t2 = Thread(target=add,args=(151,)) # 150次
    t2.setName("线程B")

    t1.start()
    t2.start()
~~~

最后，执行结果仅为150，出现了更新丢失
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3ad6eaebff5388e3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

解析出现这种事务并发问题的过程，事务A和事务B并发执行
时间| 事务A |  事务B 
-|-|-
T1 |开始事务|  |
T2 |  | 开始事务 |
T3 | 查询yk值为0 |  |
T4 |  |  查询yk值为0|
T5 | yk值加1 | |
T6 |  | yk值加1 |
T7 |事务提交，yk值为1  | `此时yk的值已经为1` |
T8 |  | 事务提交，yk值为1 ；`出现更新丢失，yk的值应该为2`|

###解决方式
**1、提升隔离级别到到serializable**
serializable能让数据库的所有事务都串行化，排队执行；此时就不存在事务A和事务B一起执行的情况了；但是这种方法是不允许的，因为serializabl级别禁止事务并发执行，这在性能上是一个很大的坑
~~~
set session transaction isolation level serializable ;
set global transaction isolation level serializable;
SELECT @@global.tx_isolation, @@tx_isolation;

~~~

重新运行上面的程序，运行结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f806aa40f324fc85.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


**2、使用悲观锁---X锁，加锁读**

重新将隔离级别设为默认级别 RR
~~~
set session transaction isolation level repeatable read ;
set global transaction isolation level repeatable read;
SELECT @@global.tx_isolation, @@tx_isolation;
~~~

将查询yk字段的select加上 for update关键字；添加X锁

>ex = connection.execute("SELECT yk FROM tb WHERE id = %(id)s `FOR UPDATE`;", id=1)



重新运行上面的程序，结果为250。X锁为排他锁，阻塞其它事务的加锁读和update、delete操作。所以B事务的查询操作会被阻塞，直到A事务提交B事务才会继续执行

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ee66653d28847bd5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



在这里有个问题: 为什么不使用S锁？
使用S锁在锁定行后面有更新操作，容易导致死锁。所以这种情况请使用X锁。我的这篇文章有讲到这点
https://www.jianshu.com/p/beddb45070bb

**3、使用乐观锁机制**


思路：在update语句中添加一个版本号做where条件，判断update语句执行的影响行数，如果为0则重新执行事务B；循环下去，直到更新成功！

1、先给tb表添加一个version版本号字段，更改完后表结构和数据如下
~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb
-- ----------------------------
DROP TABLE IF EXISTS `tb`;
CREATE TABLE `tb`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `yk` int(11) NULL DEFAULT NULL,
  `version` int(11) NOT NULL COMMENT '版本号',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb
-- ----------------------------
INSERT INTO `tb` VALUES (1, 0, 1);

SET FOREIGN_KEY_CHECKS = 1;

~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1131239e8735b0a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、update语句改成这样：

>result = connection.execute(
        "UPDATE tb SET yk = %(yk)s ,version = version +1 WHERE id = 1 and version = %(version)s;", yk=yk,
        version=version)

使用乐观锁的思想，代码改成如下所示
~~~
import threading
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(user='root', password='yk123',
                                                                        host='localhost',
                                                                        port='3306',
                                                                        database='test'),
    max_overflow=int(1),  # 超过连接池大小外最多创建的连接
    pool_size=int(5),  # 连接池大小,默认是5
    pool_timeout=int(1),  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=int(0)  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)



# 修改
def add(count):
    for i in list(range(1,count)):
        print(threading.currentThread().getName()+"==>"+str(i))
        dg()


def dg():
    connection = engine.connect(close_with_result=False)
    trans = connection.begin()
    ex = connection.execute("SELECT yk,version FROM tb WHERE id = %(id)s;", id=1)
    y = ex.first()
    version = y[1]
    yk = y[0]
    yk = yk + 1
    result = connection.execute(
        "UPDATE tb SET yk = %(yk)s ,version = version +1 WHERE id = 1 and version = %(version)s;", yk=yk,
        version=version)
    rowcount = result.rowcount
    trans.commit()

    # update影响行数为0，说明更新失败！自旋！这里做dg函数的递归调用
    if rowcount == 0:
        dg()




# 测试
if __name__ == '__main__':
    # 用线程去执行函数
    t1 = Thread(target=add,args=(101,)) # 100次
    t1.setName("线程A")

    t2 = Thread(target=add,args=(151,)) # 150次
    t2.setName("线程B")

    t1.start()
    t2.start()
~~~

执行结果：yk值最终为250
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8b728c93f9463b5f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意：自旋的递归调用一定不能在同一个事务里执行，因为mysql的默认RR级别下是允许可重复的，也就是说多次读取version字段并不会发生改变。故需要一次递归就开启一次事务，这样才能读到最新的version字段



###比较悲观锁和乐观锁，应该选择哪种？
悲观锁在查询时添加X锁，查询多效率低下
乐观锁在大量的并发修改下，很容易造成失败自旋，在我上面的例子中体现的是 dg()函数的递归执行。极端情况下要失败很多次才能成功修改

- 查询多，修改少 使用乐观锁
- 查询少，修改多 使用悲观锁

《阿里巴巴Java开发手册》里面有讲到关于悲观锁和乐观锁的选择：
>【强制】 并发修改同一记录时，避免更新丢失，需要加锁。 要么在应用层加锁，要么在缓存加锁，要么在数据库层使用乐观锁，使用 version 作为更新依据。
说明：如果每次访问冲突概率小于 20%，推荐使用乐观锁，否则使用悲观锁。乐观锁的重试次数不得小于3 次。但是如何判断`冲突概率`和`重试次数`呢？这应该根据业务环境进行实验才能得出吧

还有一条
>【推荐】 资金相关的金融敏感信息，使用悲观锁策略。
说明：乐观锁在获得锁的同时已经完成了更新操作，校验逻辑容易出现漏洞，另外，乐观锁对冲突的解决策略有较复杂的要求，处理不当容易造成系统压力或数据异常，所以`资金相关的金融敏感信息不建议使用乐观锁更新`。


###其实这种更新丢失问题可以交给mysql自己解决

我们不需要将yk字段读到程序中，给它加1再赋值回去。完全可以直接在sql中进行加1，如

>UPDATE tb SET yk = yk + 1 WHERE id = 1;

这样的sql具有原子性，本身的读和写被mysql底层看做一个操作。因此不会出现更新丢失了

~~~
import threading
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(user='root', password='yk123',
                                                                        host='localhost',
                                                                        port='3306',
                                                                        database='test'),
    max_overflow=int(1),  # 超过连接池大小外最多创建的连接
    pool_size=int(5),  # 连接池大小,默认是5
    pool_timeout=int(1),  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=int(0)  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)



# 修改
def add(count):
    for i in list(range(1,count)):
        print(threading.currentThread().getName()+"==>"+str(i))
        connection = engine.connect(close_with_result=False)
        trans = connection.begin()
        connection.execute("UPDATE tb SET yk = yk + 1 WHERE id = 1;")
        trans.commit()


# 测试
if __name__ == '__main__':
    # 用线程去执行函数
    t1 = Thread(target=add,args=(101,)) # 100次
    t1.setName("线程A")

    t2 = Thread(target=add,args=(151,)) # 150次
    t2.setName("线程B")

    t1.start()
    t2.start()
~~~
