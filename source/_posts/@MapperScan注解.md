---
title: MapperScan注解.md
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
title: @MapperScan注解.md
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
1、@Mapper注解：
作用：在接口类上添加了@Mapper，在编译之后会生成相应的接口实现类
添加位置：接口类上面

@Mapper
public interface UserDAO {
   //代码
}

如果想要每个接口都要变成实现类，那么需要在每个接口类上加上@Mapper注解，比较麻烦，解决这个问题用@MapperScan

2、@MapperScan
作用：指定要变成实现类的接口所在的包，然后包下面的所有接口在编译之后都会生成相应的实现类
添加位置：是在Springboot启动类上面添加，

@SpringBootApplication
@MapperScan("com.winter.dao")
public class SpringbootMybatisDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringbootMybatisDemoApplication.class, args);
    }
}

添加@MapperScan(“com.winter.dao”)注解以后，com.winter.dao包下面的接口类，在编译之后都会生成相应的实现类

3、使用@MapperScan注解多个包
（实际用的时候根据自己的包路径进行修改）

@SpringBootApplication  
@MapperScan({"com.kfit.demo","com.kfit.user"})  
public class App {  
    public static void main(String[] args) {  
       SpringApplication.run(App.class, args);  
    }  
} 

4、 如果dao接口类没有在Spring Boot主程序可以扫描的包或者子包下面，可以使用如下方式进行配置：
（没验证过，不确定能否使用，或许需要根据自己定义的包名进行修改路径）

@SpringBootApplication  
@MapperScan({"com.kfit.*.mapper","org.kfit.*.mapper"})  
public class App {  
    public static void main(String[] args) {  
       SpringApplication.run(App.class, args);  
    }  
} 
原文：https://blog.csdn.net/nba_linshuhao/article/details/82783454

早点的时间是直接在Mapper类上面添加注解@Mapper，这种方式要求每一个mapper类都需要添加此注解，比较麻烦。

现在通过使用@MapperScan可以指定要扫描的Mapper类的包的路径,比如:

@SpringBootApplication
@MapperScan("com.lz.water.monitor.mapper")
// 添加对mapper包扫描
public class Application {


public static void main(String[] args) {
SpringApplication.run(Application.class, args);
}

}

同时,使用@MapperScan注解多个包

 

@SpringBootApplication  
@MapperScan({"com.kfit.demo","com.kfit.user"})  
public class App {  
    public static void main(String[] args) {  
       SpringApplication.run(App.class, args);  
    }  
} 
如果如果mapper类没有在Spring Boot主程序可以扫描的包或者子包下面，可以使用如下方式进行配置

@SpringBootApplication  
@MapperScan({"com.kfit.*.mapper","org.kfit.*.mapper"})  
public class App {  
    public static void main(String[] args) {  
       SpringApplication.run(App.class, args);  
    }  
} 
 
