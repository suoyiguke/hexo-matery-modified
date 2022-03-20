---
title: java持久化-mybatis-中#{}和${}与sql注入问题（一）.md
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
title: java持久化-mybatis-中#{}和${}与sql注入问题（一）.md
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
> 大巧若拙

###\#{} 
\#{}  底层通过prepareStatement对当前传入的sql进行了预编译，一个 #{ } 被解析为一个参数占位符 `?`; \#{} 解析之后会将String类型的数据自动加上引号，其他数据类型不会;\#{} 很大程度上可以防止sql注入（sql注入是发生在编译的过程中，因为恶意注入了某些特殊字符，最后被编译成了恶意的执行操作）

这篇文章https://www.jianshu.com/p/19a9f2340ebe演示了jdbc的prepareStatement预编译防止sql注入，会给危险的单引号转义

\#{} 一般用在insert的字段和where条件中，用来防止sql注入

###\${}
\${}仅仅为一个纯粹的 string 替换，在动态sql解析阶段将会进行变量替换;\${} 解析之后是什么就是什么;

${} 用在`sql字符串拼接`中，使用时需要非常谨慎，sql注入可不是闹着玩的。但是像一些没有直接和系统用户接触的功能如动态切换表名，库名呀就不存在注入问题了。一旦要使用在要被用户直接接触的sql中，一定要注意！

######${}出现sql注入问题演示
编写mapper接口
~~~
    @Select("select * from user where name = #{name}")
    List<User> sqltest1(String name);
~~~

进行测试传入参数为 `1' OR 1='1 `
~~~

    @Test
    public void testInsert(){

        List<User> users = mapper.sqltest1("1' OR 1='1 ");
        for (User user : users) {
            System.out.println(user);

        }

    }
~~~

因为字段里main包含`单引号` ,所以最终因为\${}拼接出来的sql字符串变成了这样。所以把所有的user信息均查出来了
>select * from user where name = '1' OR 1='1 ';

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f6a585edecf281ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


那么我们使用\#{}进行对比试验，编写mapper接口
~~~
  @Select("select * from user where name = #{name}")
    List<User> sqltest1(String name);

~~~
最终的sql什么都没查到，执行结果如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-47e76d9ff07fe90a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看mysql全日志，发现`单引号被转义！`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0e4c443a141e208a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)










###动态指定order by 排序字段
mybatis排序使用order by传入列名时使用$而不是#

如果使用#，会自动给列名加上单引号，实验如下
~~~
   @Select("select * from user order by #{column}")
    List<User> sqltest1(String column);
~~~
~~~
   @Test
    public void testInsert(){

        List<User> users = mapper.sqltest1("name");

    }
~~~
执行的sql如下，此时执行排序的是一个字符串字面量，是没有任何效果的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3cc24460c15efce5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们来使用${}试试
~~~
    @Select("select * from user order by ${column}")
    List<User> sqltest1(String column);

~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b6d2ecc31753c447.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如此看来，这时候需要使用${}


###like模糊匹配

编写mapper接口
~~~
    @Select("select * from user where name like '%${name}%'")
    List<User> sqltest2(String name);
~~~
测试
~~~
    @Test
    public void testInsert(){
        List<User> users = mapper.sqltest2("yin");
        for (User user : users) {
            System.out.println(user);
        }
    }
~~~
发出sql如下，没问题
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0b9e6ff3ca134194.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用#{}做对比试验
~~~
    @Select("select * from user where name like '%#{name}%'")
    List<User> sqltest2(String name);
~~~

测试直接报错如下
>java.sql.SQLException: Parameter index out of range (1 > number of parameters, which is 0).



###总结
初步看来动态指定order by 排序字段、like模糊匹配都需要使用\${}，但是这种方式会带来sql注入问题。那我们应该如何解决？

可以看看我的这篇文章https://www.jianshu.com/p/980ec49f735c 对这两种情况的解决方案



###使用注意
尽量采用“#{}”这样的格式。若不得不使用“${}”这样的参数请做好防止sql注入的操作
