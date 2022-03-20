---
title: springboot-redis使用之实现Spring-Cache.md
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
title: springboot-redis使用之实现Spring-Cache.md
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

spring给我们提供了缓存的封装，类似于事务管理一样。可以基于注解直接开箱即用。不需要复杂的配置。而且spring cache底层实现实现可以如下方式
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f81f504af2d0ddea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


redis只是其中一种，如果工程内只配置了redis则以redis为cache的实现。所以想要实现基于redis的缓存，则需先集成redis，可以看看这篇文章 https://www.jianshu.com/p/ed4b3af12f25

基于redis的缓存实现，数据类型使用string。使用注解里的属性做redis的key，value则是加上缓存注解方法的返回值。在第一次调用该方法时即会将javabean序列化为string存入redis当做缓存，第二次再次调用会用注解的参数去redis中找key，找到了直接就将redis中的value反序列化为javabean返回。没有则生成新的缓存

###springboot cache使用示例


引入spring-boot-starter-cache依赖
~~~	
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-cache</artifactId>
</dependency>
~~~

在springboot.yml上加上配置

>- cache-names: cache1,cache2 中cache1,cache2 即是缓存的key
~~~
spring:
  cache:
    # 指定缓存类型
    type: redis
    # 指定在启动时创建缓存名称，多个名称用逗号分隔。
    cache-names: cache1,cache2
    # redis缓存实现配置
    redis:
      #缓存有效时间，单位毫秒，默认长久有效。这里是60秒失效
      time-to-live: 600000
      #是否缓存null值
      cache-null-values: true
      #在写入Redis时是否要使用key前缀
      use-key-prefix: true
      #key前缀
      key-prefix: cache_
~~~

在springboot启动类上加上@EnableCaching注解
![image.png](https://upload-images.jianshu.io/upload_images/13965490-163d0b11c269c26e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在需要缓存的实体类上实现Serializable接口
![image.png](https://upload-images.jianshu.io/upload_images/13965490-297c357ac0013186.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


如下，在一个分页查询方法中，使用了 @Cacheable 注解
>@Cacheable(value = "User", key = "#root.methodName+':'+#root.args[0]+':'+#root.args[1]")



~~~
     /**
     * 分页查询
     * @param cPage
     * @param pSize
     * @return R
     */
    @RequestMapping("/list")
    @Cacheable(value = "User", key = "#root.methodName+':'+#root.args[0]+':'+#root.args[1]")
    public R list(Integer cPage,Integer pSize){
        IPage<User> userIPage = userService.selectPage(cPage, pSize);
        return R.ok(userIPage);
    }

~~~

运行工程，访问 http://192.168.10.106:8080/test/user/list?cPage=1&pSize=10 即可生成缓存

我们来看看redis中生成的缓存
![image.png](https://upload-images.jianshu.io/upload_images/13965490-758777218888207c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######缓存的维护

如果对已缓存的持久化数据进行 添加、删除、修改操作，那么缓存就必须相应进行维护。spring 给我们提供了这个功能。
使用@CacheEvict注解，加在controller方法之上，这个方法被调用后将清除所有缓存名为User的缓存。虽然使用这个注解能够达到维护缓存的目的，可是这会将所有User上的缓存清除，而不是只清除具体id的user实体，有没有方法达到这种细粒度的控制呢?
 >@CacheEvict(value = "User", allEntries=true)
~~~
    /**
     * 根据id删除
     * @param id
     * @return R
     */
    @CacheEvict(value = "User", allEntries=true)
    @RequestMapping("/deleteById")
    public R deleteById(Integer id){
        boolean b = userService.removeById(id);
        return R.ok(b);
    }
~~~


######Spel 表达式
我们可以看到 @Cacheable注解的key属性里面可以使用Spel 表达式来确定key。可以使用root对象来获得被注解申明的方法信息，如方法名、参数名等
org.springframework.cache.interceptor.CacheExpressionRootObject类即是这个root
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a24cd40df56034cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

还可以使用这种形式，直接使用参数名
> @Cacheable(value = "User", key = "#root.methodName+':'+#cPage+':'+#pSize")


参考文档
https://docs.spring.io/spring-boot/docs/current/reference/html/boot-features-caching.html
[https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-caching-provider-redis](https://docs.spring.io/spring-boot/docs/current/reference/html/spring-boot-features.html#boot-features-caching-provider-redis)
