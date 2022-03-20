---
title: mybatis-一级缓存和它带来的问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis-一级缓存和它带来的问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
> mybatis一级缓存很可能出现脏数据！！

一级缓存是session隔离的。若sessionA 和sessionB 同时 查询。 sessionA 之后将数据修改。 sessionB再次查询还是之前的。

这个问题和事务隔离级别没有关系。是框架层面的问题。一级缓存默认存在的，如果设法关闭之即可解决。

只有在select类型的缓存中可能出现，在一个session中先后发出select可以发现只会发出一条sql。只有第一个查询会发出sql，后面的查询不会发出sql。

###问题重现
> mysql进行垂直分表，需要用一张表专门来生成唯一id。使用AUTO_INCREMENT自增的方式

创建test表
~~~
CREATE TABLE `test`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
~~~
编写存储过程 getId
~~~
CREATE DEFINER="root"@"%" PROCEDURE "getId"()
BEGIN
	
SET @@autocommit = 0;
INSERT INTO `iam`.`tlk_signed_data_id`(`id`) VALUES (NULL);
SELECT LAST_INSERT_ID()+1 id;
COMMIT;

END
~~~

dao 中定义  statement
~~~
    @Select( value = "call getId()" )
    @Options(statementType = StatementType.CALLABLE)
    Integer addOneAndGetNextId();
~~~

测试代码
~~~

    @Test
    @Rollback(false)
    @Transactional(rollbackFor = Exception.class ,isolation = Isolation.REPEATABLE_READ,propagation = Propagation.REQUIRED)
    public  void test1(){

        for (int i = 0; i <100 ; i++) {
            Integer integer = tlkSignedDataDao.addOneAndGetNextId();
            System.out.println(integer);
            tlkSignedDataDao.updateTest();
        }


    }

~~~

执行结果，发现只发出了一条sql。后面的查询复用前面的结果116。很容易想到事务的隔离级别，默认的RR下是可重复读的。但是可重复读下也是会发出sql的这不符合问题表现。推测是走了缓存。
~~~
2020-06-08 17:33:55,288 [main] DEBUG org.szwj.ca.identityauthsrv.dao.TlkSignedDataDao:62 - Cache Hit Ratio [org.szwj.ca.identityauthsrv.dao.TlkSignedDataDao]: 0.0
2020-06-08 17:33:55,297 [main] DEBUG o.s.c.i.dao.TlkSignedDataDao.addOneAndGetNextId:159 - ==>  Preparing: call getId() 
2020-06-08 17:33:55,350 [main] DEBUG o.s.c.i.dao.TlkSignedDataDao.addOneAndGetNextId:159 - ==> Parameters: 
2020-06-08 17:33:55,442 [main] DEBUG o.s.c.i.dao.TlkSignedDataDao.addOneAndGetNextId:159 - <==      Total: 1
2020-06-08 17:33:55,443 [main] DEBUG o.s.c.i.dao.TlkSignedDataDao.addOneAndGetNextId:159 - <==    Updates: 0
116
2020-06-08 17:33:55,443 [main] DEBUG org.szwj.ca.identityauthsrv.dao.TlkSignedDataDao:62 - Cache Hit Ratio [org.szwj.ca.identityauthsrv.dao.TlkSignedDataDao]: 0.0
116
~~~

###解决方式
>在select中设置flushCache=true
~~~
    @Select( value = "call getId()" )
    @Options(flushCache= FlushCachePolicy.TRUE,statementType = StatementType.CALLABLE)
~~~




###一级缓存实现源码

####缓存存储实现核心类 
可以看到一级缓存其实就是使用HashMap<Object, Object>实现的
>org.apache.ibatis.cache.impl.PerpetualCache
~~~
public class PerpetualCache implements Cache {

  private String id;

  private Map<Object, Object> cache = new HashMap<Object, Object>();
~~~

####缓存业务逻辑实现核心类
>org.apache.ibatis.executor.BaseExecutor

#####实现一级缓存的核心逻辑方法 
>org.apache.ibatis.executor.BaseExecutor#query(org.apache.ibatis.mapping.MappedStatement, java.lang.Object, org.apache.ibatis.session.RowBounds, org.apache.ibatis.session.ResultHandler, org.apache.ibatis.cache.CacheKey, org.apache.ibatis.mapping.BoundSql)
~~~
  @SuppressWarnings("unchecked")
  @Override
  public <E> List<E> query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, CacheKey key, BoundSql boundSql) throws SQLException {
    ErrorContext.instance().resource(ms.getResource()).activity("executing a query").object(ms.getId());
    if (closed) {
      throw new ExecutorException("Executor was closed.");
    }
    //ms.isFlushCacheRequired() 为true 则清除缓存！
    //org.apache.ibatis.mapping.MappedStatement#flushCacheRequired 属性就是@Options(flushCache= FlushCachePolicy.TRUE) 注解中的flushCache字段
    if (queryStack == 0 && ms.isFlushCacheRequired()) {
      clearLocalCache();
    }
    List<E> list;
    try {
      queryStack++;
     // 从localCache实现缓存的map对象中根据key查询
      list = resultHandler == null ? (List<E>) localCache.getObject(key) : null;

      if (list != null) {
        handleLocallyCachedOutputParameters(ms, key, parameter, boundSql);
      } else {
         // list结果集不为空则去数据库中查询
        list = queryFromDatabase(ms, parameter, rowBounds, resultHandler, key, boundSql);
      }
    } finally {
      queryStack--;
    }
    if (queryStack == 0) {
      for (DeferredLoad deferredLoad : deferredLoads) {
        deferredLoad.load();
      }
      // issue #601
      deferredLoads.clear();
      if (configuration.getLocalCacheScope() == LocalCacheScope.STATEMENT) {
        // issue #482
        clearLocalCache();
      }
    }
    return list;
  }

~~~

#####从库中查询
> org.apache.ibatis.executor.BaseExecutor#queryFromDatabase
~~~
  private <E> List<E> queryFromDatabase(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, CacheKey key, BoundSql boundSql) throws SQLException {
    List<E> list;
    localCache.putObject(key, EXECUTION_PLACEHOLDER);
    try {
      list = doQuery(ms, parameter, rowBounds, resultHandler, boundSql);
    } finally {
      localCache.removeObject(key);
    }
    localCache.putObject(key, list);
    if (ms.getStatementType() == StatementType.CALLABLE) {
      localOutputParameterCache.putObject(key, parameter);
    }
    return list;
  }

~~~



###总结
1、可以发现一级缓存并不是 细粒度到key级别的维护。一旦触发update，将会把所有的缓存清除。可以看源码。
>org.apache.ibatis.executor.BaseExecutor#update
~~~
  @Override
  public int update(MappedStatement ms, Object parameter) throws SQLException {
    ErrorContext.instance().resource(ms.getResource()).activity("executing an update").object(ms.getId());
    if (closed) {
      throw new ExecutorException("Executor was closed.");
    }
    //清除所有一级缓存
    clearLocalCache();
    return doUpdate(ms, parameter);
  }
~~~


上面提到的问题，还可以这样解决：
dao
~~~
   @Update(" update tlk_signed_data_id set id = -1 where id = -1 ")
    void updateTest();
~~~

测试代码
~~~
    @Test
    @Rollback(false)
    @Transactional(rollbackFor = Exception.class ,isolation = Isolation.REPEATABLE_READ,propagation = Propagation.REQUIRED)
    public  void test1(){

        for (int i = 0; i <100 ; i++) {
            Integer integer = tlkSignedDataDao.addOneAndGetNextId();
            System.out.println(integer);
           //触发修改，清除一级缓存！
            tlkSignedDataDao.updateTest();
        }


    }

~~~


2、不只是update，像 insert、delete 也行。因为最终也会调用 update。源码为证：

>org.apache.ibatis.session.defaults.DefaultSqlSession

~~~

 @Override
  public int insert(String statement, Object parameter) {
    return update(statement, parameter);
  }

  @Override
  public int delete(String statement, Object parameter) {
    return update(statement, parameter);
  }

@Override
  public int update(String statement, Object parameter) {
    try {
      dirty = true;
      MappedStatement ms = configuration.getMappedStatement(statement);
      return executor.update(ms, wrapCollection(parameter));
    } catch (Exception e) {
      throw ExceptionFactory.wrapException("Error updating database.  Cause: " + e, e);
    } finally {
      ErrorContext.instance().reset();
    }
  }
~~~

