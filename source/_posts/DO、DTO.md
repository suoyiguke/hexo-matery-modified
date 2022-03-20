---
title: DO、DTO.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 软件工程和项目管理
categories: 软件工程和项目管理
---
---
title: DO、DTO.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 软件工程和项目管理
categories: 软件工程和项目管理
---
### 何为JavaBean

JavaBean，可序列化的POJO，sun在早期有对其规范（[JavaBeans Spec](https://link.zhihu.com/?target=https%3A//www.oracle.com/technetwork/java/javase/documentation/spec-136004.html)），它是Java中的可重用组件，主要规范约定如下：

*   JavaBean为公共类，并且具有一个空构造函数
*   所有属性为私有属性，提供getter和setter，不应该有公共属性
*   实现序列化接口：`java.io.Serializable`

JavaBean已经成为Java的一种规范，也是Java社区的共同语言，许多工具框架也是遵循JavaBean的规范的，例如，Spring的BeanUtils，一些Json工具都是基于JavaBean的规范来实现的，这些都是基于约定，所以也有人把JavaBean叫为可以持久化的POJO。

### 何为DO

DO（Domain Object），领域对象，也就是ORM框架中对应数据库的对象，业务实体，例如，对现实世界中的用户建模，抽象出来的DO可以叫为UserDO，通常情况下它用于与数据库的数据交互，通常也是一个JavaBean。

### 何为PO

PO（Persistent Object），持久化对象，主要用于持久化层，与数据库对应，通常也是ORM框架中的实体对象，例如，使用JPA时候的Entity与数据库表做映射，通常是一个JavaBean。

### 何为DTO

DTO（Data Transfer Object），数据传输对象，顾名思义就是用于传输数据的对象，通常用于处于不同架构层次或者不同子系统之间的数据传递，或者用于外部接口参数传递，以便提供不同粒度不同信息的数据，以免造成困惑干扰，通常也是一个JavaBean。

### 何为VO

VO（Value Object），就是用于保存数据的对象；在提供给页面使用的时候，也有人解释为View Object，就是对应页面展示数据的对象。

### 何为DAO

DAO（Data Access Object），数据访问对象，与数据库做交互的对象，提供不同的接口访问数据库来实现对数据库的操作，而接口使用的数据交互通常就是PO或者DO，通过它可以使用面向对象的方式来与数据库交互。




数据库业务实体用 DO
数据库查询结构包装类用DTO
视图类用VO

