---
title: 在秒杀场景中spring-声明式事务与lock范围的坑.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: 在秒杀场景中spring-声明式事务与lock范围的坑.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
在减库存，生成订单的秒场景中。lock写在@Transactional声明的方法之内还是会出现线程安全问题引起超卖。

先解锁后提交事务
~~~

    @GetMapping(value = "/saveDb1")
    public GbmResult saveDb1() {
        CountDownLatch threadCountDown = new CountDownLatch(1);
        CountDownLatch mainCountDownLatch = new CountDownLatch(10000);
        ReentrantLock lock = new ReentrantLock();

        for (int i = 0; i < 10000; i++) {
            executorService.execute(() -> {
                try {
                    threadCountDown.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                dbService.saveDb(lock);
                mainCountDownLatch.countDown();
            });
        }

        threadCountDown.countDown();
        try {
            mainCountDownLatch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return GbmResult.success();
    }
~~~
~~~
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void saveDb(Lock lock) {
        lock.lock();
        try {
            //查库存
            SqlRowSet sqlRowSet = jdbcTemplate.queryForRowSet("select num from test where id = 1 limit 1");
            boolean next = sqlRowSet.next();
            if (next) {
                int num = sqlRowSet.getInt("num");
                if (num > 0) {
                    //减库存
                    jdbcTemplate.update("update test set num = num - 1 where  id = 1 limit 1");
                    //加订单
                    jdbcTemplate.execute("insert into test2(id) VALUES(1)");
                } else {
                    System.out.println(Thread.currentThread().getName() + "库存不足");
                }
            }
        } finally {
            lock.unlock();
        }

       //sleep为了放大线程安全问题便于演示
        try {
            Thread.sleep(ThreadLocalRandom.current().nextInt(1, 5000));
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
~~~

解决思路：必须先提交事务后解锁


1、把lock加锁解锁提到声明事务外层

~~~
    @GetMapping(value = "/saveDb2")
    public GbmResult saveDb2() {
        CountDownLatch threadCountDown = new CountDownLatch(1);
        CountDownLatch mainCountDownLatch = new CountDownLatch(10000);
        ReentrantLock lock = new ReentrantLock();

        for (int i = 0; i < 10000; i++) {
            executorService.execute(() -> {
                try {
                    threadCountDown.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                lock.lock();
                try {
                    dbService.saveDb2();
                } finally {
                    lock.unlock();
                }
                mainCountDownLatch.countDown();
            });
        }

        threadCountDown.countDown();
        try {
            mainCountDownLatch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return GbmResult.success();
    }

~~~


~~~
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void saveDb2() {
        //查库存
        SqlRowSet sqlRowSet = jdbcTemplate.queryForRowSet("select num from test where id = 1 limit 1");
        boolean next = sqlRowSet.next();
        if (next) {
            int num = sqlRowSet.getInt("num");
            if (num > 0) {
                //减库存
                jdbcTemplate.update("update test set num = num - 1 where  id = 1 limit 1");
                //加订单
                jdbcTemplate.execute("insert into test2(id) VALUES(1)");
            } else {
                System.out.println(Thread.currentThread().getName() + "库存不足");
            }
        }

        try {
            Thread.sleep(ThreadLocalRandom.current().nextInt(1, 5000));
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
~~~


2、直接使用编程式事务，这样事务提交时机会更加清晰
~~~
    @Override
    public void saveDb3(Lock lock, int i) {
        lock.lock();
        try {
            transactionTemplate.execute(new TransactionCallbackWithoutResult() {
                @Override
                protected void doInTransactionWithoutResult(TransactionStatus status) {
                    try {
                        //查库存
                        SqlRowSet sqlRowSet = jdbcTemplate.queryForRowSet("select num from test where id = 1 limit 1");
                        boolean next = sqlRowSet.next();
                        if (next) {
                            int num = sqlRowSet.getInt("num");
                            if (num > 0) {
                                //减库存
                                jdbcTemplate.update("update test set num = num - 1 where  id = 1 limit 1");
                                //加订单
                                jdbcTemplate.execute("insert into test2(id) VALUES(1)");
                            } else {
                                System.out.println(Thread.currentThread().getName() + "库存不足");
                            }
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                        status.setRollbackOnly();
                    }
                }
            });
        } finally {
            lock.unlock();
        }
    }
~~~






