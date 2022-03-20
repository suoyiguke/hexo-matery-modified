---
title: java-基础之合理使用if-else.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
https://juejin.im/post/5e5fa79de51d45271849e7bd

~~~
@Around("dataSourcePointCut()")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        //事实上默认数据源是 MASTER

        //得到类上的注解
        DataSource dataSourceClass = point.getTarget().getClass().getAnnotation(DataSource.class);
        //如果类上的注解的参数是SLAVE
        if(dataSourceClass != null && DataSourceNames.SLAVE.getName().equals(dataSourceClass.name())){
            //设置当前线程数据源为SLAVE
            DynamicDataSource.setDataSource(DataSourceNames.SLAVE.getName());
            logger.info("设置数据源为" + DataSourceNames.SLAVE);
        }

        //得到方法上的注解,方法上的注解优先级大于类上的
        MethodSignature signature = (MethodSignature) point.getSignature();
        Method method = signature.getMethod();
        DataSource dataSourceMethod = method.getAnnotation(DataSource.class);
        //如果类上的注解的参数是SLAVE
        if(dataSourceMethod != null && DataSourceNames.SLAVE.getName().equals(dataSourceMethod.name())){
            //设置当前线程数据源为SLAVE
            DynamicDataSource.setDataSource(DataSourceNames.SLAVE.getName());
            logger.info("设置数据源为" + DataSourceNames.SLAVE);
        }else{
            //让方法上的注解优先级大于类上的，所以需要写一个else
            //设置当前线程数据源为MASTER
            DynamicDataSource.setDataSource(DataSourceNames.MASTER.getName());
            logger.info("设置数据源为" + DataSourceNames.MASTER);
        }

        try {
            return point.proceed();
        } finally {
            DynamicDataSource.clearDataSource();
            logger.info("调用目标方法后，将数据源还原为默认");
        }
    }

~~~
