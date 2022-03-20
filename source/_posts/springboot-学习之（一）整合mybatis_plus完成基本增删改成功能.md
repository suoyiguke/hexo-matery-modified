---
title: springboot-学习之（一）整合mybatis_plus完成基本增删改成功能.md
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
title: springboot-学习之（一）整合mybatis_plus完成基本增删改成功能.md
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
准备工具：IntelliJ IDEA 
搭建目标：springboot+druid+mybatis_plus 并完成基本的增删改查功能


######创建springboot项目

1、使用idea的new project选项创建一个springboot项目
file-->new -->project
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1d1e5c923cf17e0c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
选择spring initializr，点击next
![image.png](https://upload-images.jianshu.io/upload_images/13965490-44f8e238163c08fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
填好项目一些重要的信息，继续点击next
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bc8a13160f630330.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这里可以选择springboot版本和项目中需要的依赖；我这里使用的是2.2.4版本，而项目的依赖我习惯是在pom.xml中手动修改。就先选择个spring web吧。。继续点击next
![image.png](https://upload-images.jianshu.io/upload_images/13965490-335abaf1bf2f3673.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击finish
![image.png](https://upload-images.jianshu.io/upload_images/13965490-04967ac57d049c6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
至此，一个springboot项目雏形搭建完毕~ 。 运行下试试，springboot和传统的ssm项目不同。内嵌了tomcat，所以不需要再配置了。这里直接找到main方法运行即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-013cfa9315395113.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-90b8737feb26f9fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




######整合mybatis_plus

编写pom.xml 添加一些需要的依赖
以spring-boot-starter-parent 2.2.4.RELEASE为项目的父级依赖；
添加依赖mysql驱动5.1.38、druid连接池springboot版1.1.13、lombok、mybatis-plus3.3.1、spring-boot-starter-test
~~~
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.4.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.example</groupId>
    <artifactId>springboot_study</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>springboot_study</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>


    <dependencies>
        <!--jdbc驱动，操作mysql数据库必备-->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.38</version>
        </dependency>
        <!--druid数据库连接池的springboot版本-->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.13</version>
        </dependency>
        <!--lombok优化java写法的工具-->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <scope>provided</scope>
        </dependency>

        <!--mybatis-plus的springboot版本-->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>3.3.1</version>
        </dependency>

        <!--springboot的测试框架,里面有对junit4的依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <!--springboot的web框架，引入它才能让java和web交互。可以使用@RestController注解了-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

~~~
创建几个包，注意这些包要和springboot的启动类平级，否则程序运行起来会报错，无法加载bean

![image.png](https://upload-images.jianshu.io/upload_images/13965490-acbaf2eca1735f78.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在刚才新建的config包内创建mybatis_plus的配置类MybatisPlusConfig.java
- 注意@MapperScan("com.springboot.study.demo1.mapper")注解内部的包路径指的就是mapper接口所在的包，这里可以使用*做通配符
~~~
package com.springboot.study.demo1.config;

import com.baomidou.mybatisplus.extension.plugins.PaginationInterceptor;
import com.baomidou.mybatisplus.extension.plugins.pagination.optimize.JsqlParserCountOptimize;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 *@description: mybatis_plus的配置类
 *@author: yinkai
 *@create: 2020/2/25 9:19
 */
@EnableTransactionManagement
@Configuration
@MapperScan("com.springboot.study.demo1.mapper")
public class MybatisPlusConfig {

    @Bean
    public PaginationInterceptor paginationInterceptor() {
        PaginationInterceptor paginationInterceptor = new PaginationInterceptor();
        // 设置请求的页面大于最大页后操作， true调回到首页，false 继续请求  默认false
        // paginationInterceptor.setOverflow(false);
        // 设置最大单页限制数量，默认 500 条，-1 不受限制
        // paginationInterceptor.setLimit(500);
        // 开启 count 的 join 优化,只针对部分 left join
        paginationInterceptor.setCountSqlParser(new JsqlParserCountOptimize(true));
        return paginationInterceptor;
    }
}
~~~

在entity包里添加实体类User.java
~~~
package com.springboot.study.demo1.entity;
import com.baomidou.mybatisplus.annotation.TableField;
import lombok.Data;
import lombok.experimental.Accessors;
/**
 *@description: User 实体类
 *@author: yinkai
 *@create: 2020/2/25 9:21
 */
@Data
@Accessors(chain = true)
public class User {

    private Long id;
    private String name;
    private Integer age;
    private String email;

    @TableField(exist = false)
    private Integer count;
}
~~~

在mapper包中添加UserMapper.java文件
- 接口上需要添加@Mapper注解
- 接口需要继承BaseMapper<User>，这个User泛型即是上面创建的实体类User
- mybatis_plus中可以不编写对应的xml文件
~~~
package com.springboot.study.demo1.mapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.springboot.study.demo1.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
/**
 *@description: UserMapper
 *@author: yinkai
 *@create: 2020/2/25 9:22
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {

    @Select("select * from user")
    IPage<User> selectPageVo(Page<?> page);
}

~~~

在service包中创建UserService接口
- 注意service接口继承  IService<User>；这个User泛型即是上面创建的实体类User
- 该接口类里面包含了selectPage()分页接口
~~~
package com.springboot.study.demo1.service;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.springboot.study.demo1.entity.User;
/**
 *@description: UserService
 *@author: yinkai
 *@create: 2020/2/25 9:22
 */
public interface UserService extends IService<User> {

    IPage<User> selectPage(Integer cPage, Integer pSize);
}
~~~
在service.impl包中创建UserService接口的实现类UserServiceImpl.java
- 实现类需要继承ServiceImpl<UserMapper, User> 类；UserMapper即是上面创建的mapper接口；这个User泛型即是上面创建的实体类User
- 实现UserService接口
- 注意添加@Service注解

~~~
package com.springboot.study.demo1.service.impl;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.mapper.UserMapper;
import com.springboot.study.demo1.service.UserService;
import org.springframework.stereotype.Service;
/**
 *@description: UserServiceImpl
 *@author: yinkai
 *@create: 2020/2/25 9:22
 */
@Service("userService")
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    @Override
    public IPage<User> selectPage(Integer cPage, Integer pSize) {
        Page<User> page = new Page<User>(cPage, pSize);
        IPage<User> userIPage = this.getBaseMapper().selectPageVo(page);

        return userIPage;
    }
}

~~~


删除掉默认的application.properties配置文件，使用yml文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-40d4d25cce01e4ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######编写application.yml
- context-path，设置项目的访问根路径；访问项目时就要url加上test
- port，设置内嵌tomcat的端口号为 8080
~~~
server:
  tomcat:
    uri-encoding: UTF-8
    max-threads: 1000
    min-spare-threads: 30
  port: 8080
  connection-timeout: 5000ms
  servlet:
    context-path: /test
~~~

- mapper-locations，扫描加载指定路径下的xml文件
- typeAliasesPackage，扫描指定实体类包的全限定名
~~~
#mybatis-plus
mybatis-plus:
  mapper-locations: classpath*:/mapper/**/*.xml
  #实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.springboot.study.demo1.entity
~~~

-  active， dev 指定加载的配置文件，分为三种环境dev|test|prod，所以还需要建立一个application-dev.yml文件方能完成配置
~~~
spring:
  # 环境 dev|test|prod
  profiles:
    active: dev
  servlet:
    multipart:
      max-file-size: 100MB
      max-request-size: 100MB
      enabled: true
  mvc:
    throw-exception-if-no-handler-found: true
~~~


全部的application.yml如下
~~~
# Tomcat
server:
  tomcat:
    uri-encoding: UTF-8
    max-threads: 1000
    min-spare-threads: 30
  port: 8080
  connection-timeout: 5000ms
  servlet:
    context-path: /test

spring:
  # 环境 dev|test|prod
  profiles:
    active: dev
  servlet:
    multipart:
      max-file-size: 100MB
      max-request-size: 100MB
      enabled: true
  mvc:
    throw-exception-if-no-handler-found: true

#mybatis-plus
mybatis-plus:
  mapper-locations: classpath*:/mapper/**/*.xml
  #实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.springboot.study.demo1.entity
  global-config:
    #数据库相关配置
    db-config:
      #主键类型  AUTO:"数据库ID自增", INPUT:"用户输入ID", ID_WORKER:"全局唯一ID (数字类型唯一ID)", UUID:"全局唯一ID UUID";
      id-type: AUTO
      #字段策略 IGNORED:"忽略判断",NOT_NULL:"非 NULL 判断"),NOT_EMPTY:"非空判断"
      field-strategy: NOT_NULL
      #驼峰下划线转换
      column-underline: true
      logic-delete-value: -1
      logic-not-delete-value: 0
    banner: false
  #原生配置
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: false
    call-setters-on-nulls: true
    jdbc-type-for-null: 'null'


~~~

######编写application-dev.yml配置
这里主要是druid连接池的配置，因为本地环境、测试环境、正式环境的mysql访问ip 密码都不会相同。所以会有多种配置
~~~
spring:
    datasource:
        type: com.alibaba.druid.pool.DruidDataSource
        druid:
            driver-class-name: com.mysql.jdbc.Driver
            url: jdbc:mysql://localhost:3306/jdbcstudy?allowMultiQueries=true&useUnicode=true&characterEncoding=UTF-8&useSSL=false
            username: root
            password: yk123
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

在controller包下创建UserController.java文件
~~~
package com.controller;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.api.R;
import com.entity.User;
import com.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
/**
 *@description: user控制类
 *@author: yinkai
 *@create: 2020/2/25 9:21
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;
  
    @RequestMapping("/list")
    public R list(){
        IPage<User> userIPage = userService.selectPage(1, 10);
        return R.ok(userIPage);
    }
}

~~~
######数据准备
~~~

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `age` int(11) NULL DEFAULT NULL COMMENT '年龄',
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, '小羊', 31, 'abc1@mp.com');
INSERT INTO `user` VALUES (2, '小mao', 32, 'abc2@mp.com');
INSERT INTO `user` VALUES (3, '小gou', 3, 'abc3@mp.com');
INSERT INTO `user` VALUES (4, '小niu', 344, 'abc4@mp.com');
INSERT INTO `user` VALUES (5, '小ren', 213, 'abc5@mp.com');
INSERT INTO `user` VALUES (6, '小qi', 32, 'abc6@mp.com');
INSERT INTO `user` VALUES (7, '小che', 444, 'abc7@mp.com');
INSERT INTO `user` VALUES (8, '小chuang', 3213, 'abc8@mp.com');
INSERT INTO `user` VALUES (9, '小hong', 34, 'abc9@mp.com');
INSERT INTO `user` VALUES (10, '小lv', 55, 'abc10@mp.com');
INSERT INTO `user` VALUES (11, '小wang', 366, 'abc11@mp.com');
INSERT INTO `user` VALUES (12, '小qiang', 1, 'abc21@mp.com');

SET FOREIGN_KEY_CHECKS = 1;
~~~

全部文件创建文完毕，运行springboot。访问接口
http://localhost:8080/test/user/list
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b613958308d9775.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
项目运行ok~

######添加增删改查接口
编写UserController.java文件；完成对User表的增删改查功能，这里就体现了mybatis_plus的开发效率了，普通的增删改查不需要动service和mapper。改了controller就ok了，功能实现一气呵成
~~~
package com.springboot.study.demo1.controller;

import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.api.R;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.service.UserService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import javax.annotation.Resource;
/**
 *@description: user控制类
 *@author: yinkai
 *@create: 2020/2/25 9:21
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Resource
    private UserService userService;

    /**
     * 分页查询
     * @param cPage
     * @param pSize
     * @return R
     */
    @RequestMapping("/list")
    public R list(Integer cPage,Integer pSize){
        IPage<User> userIPage = userService.selectPage(cPage, pSize);
        return R.ok(userIPage);
    }

    /**
     * 根据id查询
     * @param id
     * @return R
     */
    @RequestMapping("/getById")
    public R getById(Integer id){
        User IPage = userService.getById(id);
        return R.ok(IPage);
    }

    /**
     * 根据id删除
     * @param id
     * @return R
     */
    @RequestMapping("/deleteById")
    public R deleteById(Integer id){
        boolean b = userService.removeById(id);
        return R.ok(b);
    }

    /**
     * 根据id修改
     * @param id
     * @param name
     * @param age
     * @param email
     * @return R
     */
    @RequestMapping("/updateByid")
    public R updateByid(Integer id,String name,Integer age,String email){
        boolean b = userService.update(
                new UpdateWrapper<User>().set("name",name).set("age",age).set("email",email).eq("id",id)
        );
        return R.ok(b);
    }

    @RequestMapping("/addUser")
    public R addUser(String name,Integer age,String email){

        boolean save = userService.save(new User().setAge(age).setName(name).setEmail(email));
        return R.ok(save);
    }
}

~~~
