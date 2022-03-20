---
title: mybatis-源码之-SqlSession线程不安全解决.md
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
title: mybatis-源码之-SqlSession线程不安全解决.md
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
###默认使用的session工厂类:DefaultSqlSessionFactory
org.apache.ibatis.session.defaults.DefaultSqlSessionFactory#openSessionFromDataSource

~~~

  private SqlSession openSessionFromDataSource(ExecutorType execType, TransactionIsolationLevel level, boolean autoCommit) {
    Transaction tx = null;
    try {
      final Environment environment = configuration.getEnvironment();
      final TransactionFactory transactionFactory = getTransactionFactoryFromEnvironment(environment);
      tx = transactionFactory.newTransaction(environment.getDataSource(), level, autoCommit);
      final Executor executor = configuration.newExecutor(tx, execType);
      return new DefaultSqlSession(configuration, executor, autoCommit);
    } catch (Exception e) {
      closeTransaction(tx); // may have fetched a connection so lets call close()
      throw ExceptionFactory.wrapException("Error opening session.  Cause: " + e, e);
    } finally {
      ErrorContext.instance().reset();
    }
  }

~~~

org.apache.ibatis.session.defaults.DefaultSqlSessionFactory#openSessionFromConnection
~~~
  private SqlSession openSessionFromConnection(ExecutorType execType, Connection connection) {
    try {
      boolean autoCommit;
      try {
        autoCommit = connection.getAutoCommit();
      } catch (SQLException e) {
        // Failover to true, as most poor drivers
        // or databases won't support transactions
        autoCommit = true;
      }
      final Environment environment = configuration.getEnvironment();
      final TransactionFactory transactionFactory = getTransactionFactoryFromEnvironment(environment);
      final Transaction tx = transactionFactory.newTransaction(connection);
      final Executor executor = configuration.newExecutor(tx, execType);
      return new DefaultSqlSession(configuration, executor, autoCommit);
    } catch (Exception e) {
      throw ExceptionFactory.wrapException("Error opening session.  Cause: " + e, e);
    } finally {
      ErrorContext.instance().reset();
    }
  }

~~~

>一种是通过数据源获取数据库连接，并创建Executor对象及DefaultSqlSession对象。
另一种是用户提供数据库连接对象，然后DefaultSqlSessionFactory使用该连接进行创建操作。


###优化类：SqlSessionManager类
org.apache.ibatis.session.SqlSessionManager.SqlSessionInterceptor#invoke
~~~
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
      final SqlSession sqlSession = SqlSessionManager.this.localSqlSession.get();
      if (sqlSession != null) {
        try {
          return method.invoke(sqlSession, args);
        } catch (Throwable t) {
          throw ExceptionUtil.unwrapThrowable(t);
        }
      } else {
        try (SqlSession autoSqlSession = openSession()) {
          try {
            final Object result = method.invoke(autoSqlSession, args);
            autoSqlSession.commit();
            return result;
          } catch (Throwable t) {
            autoSqlSession.rollback();
            throw ExceptionUtil.unwrapThrowable(t);
          }
        }
      }
    }
~~~





SqlSessionManager提供了两种模式：

>第一种与DefaultSqlSessionFactory相同，同一线程每次通过SqlSessionManager对象访问数据库时，都会创建新的DefaultSqlSession对象来完成对数据库的操作；
第二种是SqlSessionManager通过localSqlSession变量，记录来与当前线程绑定的SqlSession对象，供当前线程循环使用，从而避免在同一线程多次创建SqlSession对象带来的性能损失。


###复用SqlSession代码
~~~
inputStream = Resources.getResourceAsStream(resource);
// 构建sqlSession工厂
//SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
SqlSessionManager sessionManager = SqlSessionManager.newInstance(inputStream);
sessionManager.startManagedSession();
String statement = "com.mapper.IStudentMapper.getAll";
List<Student> student = sessionManager.selectList(statement);
~~~
