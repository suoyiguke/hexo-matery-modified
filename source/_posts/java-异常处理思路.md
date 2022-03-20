---
title: java-异常处理思路.md
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
什么时候只需打印异常信息，什么时候又需要抛出异常？

1、影响正常业务流程的异常做抛出自定义异常处理
   像是参数非空判断、重要业务文件io流异常、


2、不影响正常业务流程的异常只需打印一下异常日志
 像是 记录操作日志到数据库、删除中间生成的临时文件捕获的异常就是属于这类不影响正常业务流程的！
