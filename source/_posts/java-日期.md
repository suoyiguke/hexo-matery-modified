---
title: java-日期.md
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
###注意
【强制】 SimpleDateFormat 是线程不安全的类，一般不要定义为 static 变量，如果定义为
static，必须加锁，或者使用 DateUtils 工具类。
正例：注意线程安全，使用 DateUtils。亦推荐如下处理：
private static final ThreadLocal<DateFormat> df = new ThreadLocal<DateFormat>() {
@Override
protected DateFormat initialValue() {
return new SimpleDateFormat("yyyy-MM-dd");
}
};
说明：如果是 JDK8 的应用，可以使用 Instant 代替 Date，LocalDateTime 代替 Calendar，
DateTimeFormatter 代替 SimpleDateFormat，官方给出的解释：simple beautiful strong immutable
thread-safe。

###字符串日期比较大小
~~~
String cd = DateUtils.getCurrentDate();// 获得当前日期

DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
if(dateFormat.parse(cd).getTime() < dateFormat.parse("2019-01-05").getTime()){
    System.out.println(213);
}else{
    System.out.println(321);

}
~~~
