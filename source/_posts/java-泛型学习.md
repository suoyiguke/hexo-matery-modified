---
title: java-泛型学习.md
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
1、返回值泛型

~~~
1\. 服务提供者 函数： 

//通过<T>声明告诉JVM返回值定义一个泛型 T        

//// 这里的T只是个占位符的效果，26个字母随便写哪个字母都可以，但一定要是和< >里面相同的字母，这里使用T

public <T> T findList(String sqlID,Map<String,Object> params) {

String statement = "com.mybatis.mapping.userMapper."+sqlID;//映射sql的标识字符串

return (T) this.session.selectList(statement, params);
}

2\. 服务调用者 函数：

//这里接收的类型声明直接写真实的类型就可以，无需强制转换

List<SubsHis> list = jdbc.findList("getSubsHisList", map);

分类: [工作总结](https://www.cnblogs.com/jpfss/category/992649.html), [开发经验](https://www.cnblogs.com/jpfss/category/992650.html)

~~~
