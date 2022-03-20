---
title: mybatis-plus配置.md
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
title: mybatis-plus配置.md
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
#mybatis-plus配置
mybatis-plus:
  #Mapper
  mapper-locations: classpath*:mapper/**/*Mapper.xml
  type-aliases-package: com.ruoyi.**.domain
   type-handlers-package: com.gbm.cloud.treasure.entity.handler



1、type-aliases-package 指定实体类包。这样在mapper中可以直接使用实体类名，不需要加包名了。很方便
其中 classpath*指的是在所有子工程的classpath下找。因为mapper文件在不同的mavan moudle中都存在一部分

2、mapper-locations: 寻找mapper文件


3、@MapperScan("com.ruoyi.**.mapper") 寻找mapper.jar 这样接口上就不用加@Mapper了，方便

4、 type-handlers-package:  寻找handlers类，handlers就是做数据类型转换的类比如说List<Img> 的转换

5、mybatis-plus.typeEnumsPackage:  寻找枚举映射到dbd的枚举类，如果某个枚举类没找到。那么数据库不会认识。insert会报错


mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.gbm.cloud.treasure.entity
  type-handlers-package: com.gbm.cloud.treasure.entity.handler
  configuration:
    map-underscore-to-camel-case: true
    call-setters-on-nulls: true

#mybatis
mybatis-plus:
  typeEnumsPackage: com.gbm.cloud.treasure.entity.*
  mapper-locations: classpath:mapper/*.xml
  typeAliasesPackage: com.gbm.cloud.treasure.entity
  global-config:
    #数据库相关配置
    db-config:
      #主键类型  AUTO:"数据库ID自增", INPUT:"用户输入ID", ID_WORKER:"全局唯一ID (数字类型唯一ID)", UUID:"全局唯一ID UUID";
      id-type: AUTO
      logic-delete-value: -1
      logic-not-delete-value: 0
    banner: false
  #原生配置
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: false
    call-setters-on-nulls: true
    jdbc-type-for-null: 'null'
