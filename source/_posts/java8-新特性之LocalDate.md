---
title: java8-新特性之LocalDate.md
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
这是对java.util.Date强有力的补充，解决了 Date 类的大部分痛点：

- 非线程安全
- 时区处理麻烦
- 各种格式化、和时间计算繁琐
- 设计有缺陷，Date 类同时包含日期和时间；还有一个 java.sql.Date，容易混淆。


java.util.Date 既包含日期又包含时间，而 java.time 把它们进行了分离：
- LocalDateTime.class //日期+时间 format: yyyy-MM-ddTHH:mm:ss.SSS
- LocalDate.class //日期 format: yyyy-MM-dd
- LocalTime.class //时间 format: HH:mm:ss



###格式化时间format
~~~
    public static void main(String[] args) {
        //format yyyy-MM-dd
        LocalDate date = LocalDate.now();
        System.out.println(String.format("date format : %s", date));

        //format HH:mm:ss
        LocalTime time = LocalTime.now().withNano(0);
        System.out.println(String.format("time format : %s", time));

        //format yyyy-MM-dd HH:mm:ss
        LocalDateTime dateTime = LocalDateTime.now();
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String format = dateTimeFormatter.format(dateTime);
        System.out.println(String.format("dateTime format : %s", format));
    }
~~~

###字符串/数字转时间parse
~~~
    public static void main(String[] args) {
        LocalDate date = LocalDate.of(2021, 1, 26);
        System.out.println(date);
        LocalDate parse = LocalDate.parse("2021-01-26");
        System.out.println(parse);

        LocalTime time = LocalTime.of(12, 12, 22);
        LocalTime parse1 = LocalTime.parse("12:12:22");
        System.out.println(time);
        System.out.println(parse1);

        LocalDateTime dateTime = LocalDateTime.of(2021, 1, 26, 12, 12, 22);
        LocalDateTime parse2 = LocalDateTime.parse("2021-01-26T12:12:22");
        System.out.println(dateTime);
        System.out.println(parse2);
    }
~~~




###计算年龄
~~~
    public static void main(String[] args) {
        LocalDate date1 = LocalDate.now();
        LocalDate date2 = LocalDate.of(1997, 6, 27);
        int age = date2.until(date1).getYears();
        System.out.println(age);

    }
~~~


###date与LocalDate
~~~
1.Date转换成LocalDate
    public static LocalDate date2LocalDate(Date date) {
        if(null == date) {
            return null;
        }
        return date.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
    }

2.LocalDate转换成Date

    public static Date localDate2Date(LocalDate localDate) {
        if(null == localDate) {
            return null;
        }
        ZonedDateTime zonedDateTime = localDate.atStartOfDay(ZoneId.systemDefault());
        return Date.from(zonedDateTime.toInstant());
    }

2.LocalDateTime转换成Date
    public static Date localDateTime2Date(LocalDateTime localDateTime) {
        return Date.from(localDateTime.atZone(ZoneId.systemDefault()).toInstant());
    }

3.LocalDate格式化
    public static String formatDate(Date date) {
        LocalDate localDate = date.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
        return localDate.format(DateTimeFormatter.ofPattern("yyyy-MM-dd"));
    }
~~~


java.time.temporal.TemporalAdjusters 里面还有很多便捷的算法，这里就不带大家看 Api 了，都很简单，看了秒懂。



###JDBC 和 java8
现在 jdbc 时间类型和 java8 时间类型对应关系是
Date ---> LocalDate
Time ---> LocalTime
TimesSamp ---> LocalDateTime

而之前统统对应 Date，也只有 Date。



获取指定时间
~~~
        Calendar calendar2 = Calendar.getInstance();
        calendar2.set(calendar2.get(Calendar.YEAR), calendar2.get(Calendar.MONTH), calendar2.get(Calendar.DAY_OF_MONTH),
                17, 00, 00);
        final DateTime of = DateTime.of(calendar2);


        LocalDateTime ldt = LocalDateTime.of(LocalDate.now(), LocalTime.of(17,0));
        System.out.println(ldt);
~~~
