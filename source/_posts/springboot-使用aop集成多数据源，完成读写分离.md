---
title: springboot-使用aop集成多数据源，完成读写分离.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot-使用aop集成多数据源，完成读写分离.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
之前有讲过面向界面编程可以将一些复用的代码封装成切面，然后通过4种通知来织入切点。从而达到降低模板代码和业务代码耦合的目的。而切换数据源也是一种模板代码，能够被封装成切面。

那么就能实现一种功能：使用自定义注解对方法或类进行申明，通过注解的方式切换数据源，实现数据库读写分离

###使用aop的方式实现切换数据源功能

编辑application-dev.yml，添加两个数据源节点 master 和 slave
~~~
spring:
    datasource:
        type: com.alibaba.druid.pool.DruidDataSource
        driver-class-name: com.p6spy.engine.spy.P6SpyDriver
        druid:
            master:
                url: jdbc:p6spy:mysql://192.168.10.11:33065/jdbcstudy?allowMultiQueries=true&useUnicode=true&characterEncoding=UTF-8&useSSL=false
                username: root
                password: root
                initial-size: 10
                max-active: 100
                min-idle: 10
                max-wait: 60000
                pool-prepared-statements: true
                max-pool-prepared-statement-per-connection-size: 20
                time-between-eviction-runs-millis: 60000
                min-evictable-idle-time-millis: 300000
                test-while-idle: true
                test-on-borrow: false
                test-on-return: false
                validationQuery: SELECT 1
                stat-view-servlet:
                    enabled: true
                    url-pattern: /druid/*
                    login-username: admin
                    login-password: admin
                filter:
                    stat:
                        log-slow-sql: true
                        slow-sql-millis: 1000
                        merge-sql: false
                    wall:
                        config:
                            multi-statement-allow: true

            slave:
                url: jdbc:p6spy:mysql://192.168.10.11:33066/jdbcstudy?allowMultiQueries=true&useUnicode=true&characterEncoding=UTF-8&useSSL=false
                username: root
                password: root
                initial-size: 10
                max-active: 100
                min-idle: 10
                max-wait: 60000
                pool-prepared-statements: true
                max-pool-prepared-statement-per-connection-size: 20
                time-between-eviction-runs-millis: 60000
                min-evictable-idle-time-millis: 300000
                test-while-idle: true
                test-on-borrow: false
                test-on-return: false
                validationQuery: SELECT 1
                stat-view-servlet:
                    enabled: true
                    url-pattern: /druid/*
                    login-username: admin
                    login-password: admin
                filter:
                    stat:
                        log-slow-sql: true
                        slow-sql-millis: 1000
                        merge-sql: false
                    wall:
                        config:
                            multi-statement-allow: true


~~~

######创建DataSourceNames接口，里面定义两个`数据源关键字`常量
~~~
package com.springboot.study.demo1.datasources;

/**
 *@description: DataSourceNames
 *@author: yinkai
 *@create: 2020/2/28 13:11
 */
public interface DataSourceNames {
    String MASTER = "master";
    String SLAVE = "slave";
}
~~~

######创建配置类 DynamicDataSource 绑定`数据源关键字`和AbstractRoutingDataSource 类的关系
>-  这里维护了一个ThreadLocal<String>。为每一个线程都绑定一个数据源关键字。最终是在重写的determineCurrentLookupKey()方法里调用 get()获得数据源关键字
>-  该类需要继承AbstractRoutingDataSource;父类的内部维护了一个名为targetDataSources的Map，并提供的setter方法用于设置数据源关键字与数据源的关系
>- 添加DynamicDataSource的构造器，里面需要调用父类的super.setDefaultTargetDataSource()、super.setTargetDataSources()、super.afterPropertiesSet()
>- 重写determineCurrentLookupKey方法，由此方法的返回值决定具体从哪个数据源中获取连接。（返回值从threadLocal中取得）
>- 对外暴露setDataSource()和clearDataSource()方法；用户设置数据源关键字和清空数据源关键字
~~~
package com.springboot.study.demo1.datasources;
import org.springframework.jdbc.datasource.lookup.AbstractRoutingDataSource;
import javax.sql.DataSource;
import java.util.Map;
/**
 *@description: DynamicDataSource类继承AbstractRoutingDataSource类；AbstractRoutingDataSource的内部维护了一个名为targetDataSources的Map，
 *并提供的setter方法用于设置数据源关键字与数据源的关系
 *@author: yinkai
 *@create: 2020/2/28 13:23
 */
public class DynamicDataSource extends AbstractRoutingDataSource {
    /**
     * 这里维护了一个ThreadLocal，为每一个线程都绑定一个数据源关键字。
     * 最终是在重写的determineCurrentLookupKey()方法里调用 get()获得数据源关键字
     */
    private static final ThreadLocal<String> threadLocal = new ThreadLocal<>();

    /**
     * DynamicDataSource构造器，
     * @param defaultTargetDataSource
     * @param targetDataSources
     */
    public DynamicDataSource(DataSource defaultTargetDataSource, Map<Object, Object> targetDataSources) {
        //设置默认数据源
        super.setDefaultTargetDataSource(defaultTargetDataSource);
        //设置数据源集合
        super.setTargetDataSources(targetDataSources);
        super.afterPropertiesSet();
    }

    /**
     * 重写determineCurrentLookupKey方法，由此方法的返回值决定具体从哪个数据源中获取连接。
     * 返回值从threadLocal中取得
     */
    @Override
    protected Object determineCurrentLookupKey() {
        return getDataSource();
    }


    /**
     * 设置数据源关键字
     */
    public static void setDataSource(String dataSource) {
        threadLocal.set(dataSource);
    }

    /**
     * 获得数据源关键字
     * @return
     */
    public static String getDataSource() {
        return threadLocal.get();
    }

    /**
     * 清空数据源关键字
     */
    public static void clearDataSource() {
        threadLocal.remove();
    }
}

~~~

######创建配置类DynamicDataSourceConfig，绑定`数据源关键字`和`数据源`
~~~
package com.springboot.study.demo1.datasources;
import com.alibaba.druid.spring.boot.autoconfigure.DruidDataSourceBuilder;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

/**
 *@description: DynamicDataSourceConfig类。Druid连接池中 数据源关键字和数据源之间的关系、
 *@author: yinkai
 *@create: 2020/2/28 13:21
 */
@Configuration
public class DynamicDataSourceConfig {

    /**
     * 读取yml文件中的master源
     */
    @Bean
    @ConfigurationProperties("spring.datasource.druid.master")
    public DataSource firstDataSource(){
        return DruidDataSourceBuilder.create().build();
    }

    /**
     * 读取yml文件中的slave源
     */
    @Bean
    @ConfigurationProperties("spring.datasource.druid.slave")
    public DataSource secondDataSource(){
        return DruidDataSourceBuilder.create().build();
    }

    @Bean
    //默认优先选择这种方式注入数据源
    @Primary
    public DynamicDataSource dataSource(DataSource firstDataSource, DataSource secondDataSource) {
        //创建一个map做数据源关键字和数据源之间的映射
        Map<Object, Object> targetDataSources = new HashMap<>();
        //put方法，key为数据源关键字、value为数据源
        targetDataSources.put(DataSourceNames.MASTER, firstDataSource);
        targetDataSources.put(DataSourceNames.SLAVE, secondDataSource);
        //以firstDataSource数据源为默认数据源，构造DynamicDataSource
        return new DynamicDataSource(firstDataSource, targetDataSources);
    }
}

~~~


######创建@DataSource注解。可以用于类和方法上、运行时有效
~~~
package com.springboot.study.demo1.datasources.annotation;
import com.springboot.study.demo1.datasources.DataSourceNames;
import java.lang.annotation.*;


/**
 *@description: DataSource
 *@author: yinkai
 *@create: 2020/2/28 13:10
 */
@Target({ElementType.METHOD,ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface DataSource {
    //默认是 MASTER
    String name() default DataSourceNames.MASTER;
}

~~~


######创建切面类
>- 切点表达式为 @within(com.springboot.study.demo1.datasources.annotation.DataSource)。表示使用该注解完成切入。而且该注解可以同时使用在类和方法上
>- 在环绕通知方法around()中让方法级别的注解优先于类级别的。如果只在类上使用类注解，则下面的方法按照类注解来使用相应的数据源

~~~
package com.springboot.study.demo1.datasources.aspect;

import com.springboot.study.demo1.datasources.DataSourceNames;
import com.springboot.study.demo1.datasources.DynamicDataSource;
import com.springboot.study.demo1.datasources.annotation.DataSource;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;
import java.lang.reflect.Method;

/**
 *@description: DataSourceAspect 多数据源，切面处理类
 *@author: yinkai
 *@create: 2020/2/28 14:28
 */
@Aspect
@Component
public class DataSourceAspect implements Ordered {
    private Logger logger = LoggerFactory.getLogger(getClass());

    @Pointcut("@within(com.springboot.study.demo1.datasources.annotation.DataSource)")
    public void dataSourcePointCut() {

    }

    @Around("dataSourcePointCut()")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        //事实上默认数据源是 MASTER

        //得到类上的注解
        DataSource dataSourceClass = point.getTarget().getClass().getAnnotation(DataSource.class);
        //如果类上的注解的参数是SLAVE
        if(dataSourceClass != null && DataSourceNames.SLAVE.equals(dataSourceClass.name())){
            //设置当前线程数据源为SLAVE
            DynamicDataSource.setDataSource(DataSourceNames.SLAVE);
            logger.info("类上设置数据源为" + DataSourceNames.SLAVE);
        }

        //得到方法上的注解,方法上的注解优先级大于类上的
        MethodSignature signature = (MethodSignature) point.getSignature();
        Method method = signature.getMethod();
        DataSource dataSourceMethod = method.getAnnotation(DataSource.class);
        //如果类上的注解的参数是SLAVE
        if(dataSourceMethod != null && DataSourceNames.SLAVE.equals(dataSourceMethod.name())){
            //设置当前线程数据源为SLAVE
            DynamicDataSource.setDataSource(DataSourceNames.SLAVE);
            logger.info("方法上设置数据源为" + DataSourceNames.SLAVE);
        }else{
            //让方法上的注解优先级大于类上的，所以需要写一个else
            //设置当前线程数据源为MASTER
            DynamicDataSource.setDataSource(DataSourceNames.MASTER);
            logger.info("方法上设置数据源为" + DataSourceNames.MASTER);
        }

        try {
            return point.proceed();
        } finally {
            DynamicDataSource.clearDataSource();
            logger.info("调用目标方法后，将数据源还原为默认的master");
        }
    }

    @Override
    public int getOrder() {
        return 1;
    }
}

~~~


###进一步实现mysql读写分离


既然可以通过注解来切换数据源，那么就可以将查操作的数据源设置为slave；增、改、删操作就作用于master。其中master和slave做了主从，对master的写就会同步到salve。关于mysql的主从复制实现，我的这篇文章有讲
 https://www.jianshu.com/p/

>- 现在只需要在查操作方法上添加@DataSource(name="slave")注解
>- 增、改、删操作方法上添加@DataSource(name="master")注解即可
>- 这种方式实现的读写分离需要在代码中维护，仅限于一主一从。超过这个数量不好去负载均衡到每台mysql，这时候就需要使用`中间件`
~~~
package com.springboot.study.demo1.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.springboot.study.demo1.datasources.annotation.DataSource;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.mapper.UserMapper;
import com.springboot.study.demo1.service.UserService;
import org.springframework.stereotype.Service;

/**
 *@description: UserServiceImpl
 *@author: yinkai
 *@create: 2020/2/25 9:22
 */
@Service
@DataSource(name="master")
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    /**
     * 读操作，使用salve数据源
     * @param cPage
     * @param pSize
     * @return
     */

    @Override
    @DataSource(name="slave")
    public IPage<User> selectPage(Integer cPage, Integer pSize) {
        Page<User> page = new Page<User>(cPage, pSize);
        IPage<User> userIPage = this.getBaseMapper().selectPageVo(page);

        return userIPage;
    }

    /**
     * 写操作，使用master数据源
     * @param user
     * @return
     */
    @Override
    @DataSource(name="master")
    public Boolean insertUser(User user){
        return save(user);
    }

}

~~~

代码地址 https://github.com/suoyiguke/springboot_study 喜欢的话就点个star吧
