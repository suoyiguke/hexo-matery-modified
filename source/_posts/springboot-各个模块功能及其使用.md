---
title: springboot-各个模块功能及其使用.md
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
title: springboot-各个模块功能及其使用.md
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
首先开发一个springboot项目需要继承spring-boot-starter-parent的依赖，然后具体的依赖`按需加载`
~~~
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.1.3.RELEASE</version>
	</parent>
~~~

1、spring-boot-starter
springboot的核心依赖，包括自动配置支持，日志、YAML。开发springboot项目必须添加这个依赖。不过，在其它依赖里也间接依赖了它，可以不去配置

~~~
<!--springboot 核心依赖-->
<dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter</artifactId>
</dependency>
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7b77488bff454dc6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、spring-boot-starter-web
提供java和web的交互接口，使用此模块可以用来开发web api。包括了tomcat服务器和spring-webmvc;此模块自动依赖了`spring-boot-starter` 所以在maven中可以不加`spring-boot-starter`
~~~
<!--springboot的web框架，引入它才能让java和web交互。可以使用@RestController注解了-->
<dependency>
       <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
</dependency>
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a0c2af25ca1f8d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、spring-boot-starter-jdbc

默认情况下，如果我们没有配置任何 DataSource，那么，SpringBoot 会为我们自动配置一个基于嵌入式数据库的 DataSource，这种自动配置行为其实很适合于测试场景，但对实际的开发帮助不大，`基本上我们会自己配置一个 DataSource 实例`，或者通过自动配置模块提供的配置参数对 DataSource 实例进行自定义的配置。这个模块不会用在实际开发中

4、spring-boot-starter-test
springboot的测试框架,里面有对junit4的依赖；springboot的测试注解@SpringBootTest就定义在此包中
~~~
        <!--springboot的测试框架,里面有对junit4的依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
~~~


5、spring-boot-starter-data-jpa
java持久化API,包括spring-data-jpa、spring-orm和hibernate；我接触的项目都是使用mybatis的，所以这个依赖没有使用过
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ca27a607e8b3a811.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


6、spring-boot-starter-actuator
用于监控和管理应用
~~~
       <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-53df61c368ab0066.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



7、spring-boot-starter-aop
面向切面编程，spring-aop、AspectJ；@Aspect、@Pointcut、@Around注解均在此依赖中




8、spring-boot-starter-security
安全框架，对spring-security支持
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d1ac47960539322f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


9、spring-boot-configuration-processor
spring默认使用yml中的配置，但有时候要用传统的xml或properties配置，就需要使用spring-boot-configuration-processor了。


~~~
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-configuration-processor</artifactId>
			<optional>true</optional>
		</dependency>
~~~


10、spring-boot-devtools
springboot热更新
~~~
      <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
        </dependency>
~~~
