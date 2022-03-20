---
title: Seata----分布式事务框架-四大工作模式.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 分布式事务
categories: 分布式事务
---
---
title: Seata----分布式事务框架-四大工作模式.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 分布式事务
categories: 分布式事务
---
http://seata.io/zh-cn/

####AT 模式
> AT 模式到对业务的无侵入 ，是学习的主要目标！

基于 **支持本地 ACID 事务** 的 **关系型数据库**：

*   一阶段 prepare 行为：在本地事务中，一并提交业务数据更新和相应回滚日志记录。
*   二阶段 commit 行为：马上成功结束，**自动** 异步批量清理回滚日志。
*   二阶段 rollback 行为：通过回滚日志，**自动** 生成补偿操作，完成数据回滚。




今年 1 月份，Seata 开源了 AT 模式。AT 模式是一种无侵入的分布式事务解决方案。在 AT 模式下，用户只需关注自己的“业务 SQL”，用户的 “业务 SQL” 作为一阶段，Seata 框架会自动生成事务的二阶段提交和回滚操作。

![AT 模式](https://upload-images.jianshu.io/upload_images/13965490-60b6dd6196e62803.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##### AT 模式如何做到对业务的无侵入 ：

*   一阶段：

在一阶段，Seata 会拦截“业务 SQL”，首先解析 SQL 语义，找到“业务 SQL”要更新的业务数据，在业务数据被更新前，将其保存成“before image”，然后执行“业务 SQL”更新业务数据，在业务数据更新之后，再将其保存成“after image”，最后生成行锁。以上操作全部在一个数据库事务内完成，这样保证了一阶段操作的原子性。

![AT 模式一阶段](https://upload-images.jianshu.io/upload_images/13965490-ad64845e7c0ee65d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   二阶段提交：

二阶段如果是提交的话，因为“业务 SQL”在一阶段已经提交至数据库， 所以 Seata 框架只需将一阶段保存的快照数据和行锁删掉，完成数据清理即可。

![AT 模式二阶段提交](https://upload-images.jianshu.io/upload_images/13965490-981ee6e7d394b15f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   二阶段回滚：

二阶段如果是回滚的话，Seata 就需要回滚一阶段已经执行的“业务 SQL”，还原业务数据。回滚方式便是用“before image”还原业务数据；但在还原前要首先要校验脏写，对比“数据库当前业务数据”和 “after image”，如果两份数据完全一致就说明没有脏写，可以还原业务数据，如果不一致就说明有脏写，出现脏写就需要转人工处理。

![AT 模式二阶段回滚](https://upload-images.jianshu.io/upload_images/13965490-1e547cc6ead2d440.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

AT 模式的一阶段、二阶段提交和回滚均由 Seata 框架自动生成，用户只需编写“业务 SQL”，便能轻松接入分布式事务，AT 模式是一种对业务无任何侵入的分布式事务解决方案。







####TCC 模式
2019 年 3 月份，Seata 开源了 TCC 模式，该模式由蚂蚁金服贡献。TCC 模式需要用户根据自己的业务场景实现 Try、Confirm 和 Cancel 三个操作；事务发起方在一阶段执行 Try 方式，在二阶段提交执行 Confirm 方法，二阶段回滚执行 Cancel 方法。


用户接入 TCC 模式，最重要的事情就是考虑如何将业务模型拆成 2 阶段，实现成 TCC 的 3 个方法，并且保证 Try 成功 Confirm 一定能成功。相对于 AT 模式，TCC 模式对业务代码有一定的侵入性，但是 TCC 模式无 AT 模式的全局行锁，TCC 性能会比 AT 模式高很多。




####XA模式
支持XA 事务的数据库。
Java 应用，通过 JDBC 访问数据库。

####Saga模式
Saga模式是SEATA提供的长事务解决方案，在Saga模式中，业务流程中每个参与者都提交本地事务，当出现某一个参与者失败则补偿前面已经成功的参与者，一阶段正向服务和二阶段补偿服务都由业务开发实现。



