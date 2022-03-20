---
title: java持久化框架-mybatis使用笔记.md
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
title: java持久化框架-mybatis使用笔记.md
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
1、@Param("name")参数注解的必要性
这样写在window开发环境下没问题
~~~
 @Select("select * from user where name = #{name} and password = #{password}")
  User selectUserByNameAndPassword(String name,String password);

~~~

如果把代码push到线上的linux，就会报错如下
> nested exception is org.mybatis.spring.MyBatisSystemException: nested exception is org.apache.ibatis.binding.BindingException: Parameter 'name' not found. Available parameters are [arg1, arg0, param1, param2]] with root cause
jdk_1  | org.apache.ibatis.binding.BindingException: Parameter 'name' not found. Available parameters are [arg1, arg0, param1, param2]


所以mapper要做如下修改，添加@Param("name") 注解
~~~
@Select("select * from user where name = #{name} and password = #{password}")
    User selectUserByNameAndPassword(@Param("name") String name,@Param("password") String password);

~~~

2、注解
忽略属性字段
~~~
@TableField(exist = false)
~~~


3、一对多核一对一、多对多
https://www.cnblogs.com/wenwuxianren/p/11032180.html
