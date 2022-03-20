---
title: hutool-常用记录.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: hutool-常用记录.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
https://www.hutool.cn/docs/#/

###常用的ObjectUtil
ObjectUtil.contains 有空指针处理所以比一般的contains 好用
ObjectUtil.defaultIfBlank
ObjectUtil.equal 比 Object.equal 更好用，但是也要注意 Integer和Long比较的问题
>obj1 == null && obj2 == null
obj1.equals(obj2)
如果是BigDecimal比较，0 == obj1.compareTo(obj2)

ObjectUtil.isEmpty 所有对象类型的判空方法
>判断指定对象是否为空，支持：
	   1. CharSequence
	   2. Map
	   3. Iterable
	   4. Iterator
	   5. Array

ObjectUtil.isBasicType 是否为基本类型，包括包装类型和非包装类型
ObjectUtil.IsValidIfNumber 检查是否为有效的数字
ObjectUtil.emptyCount 返回空对象数

>存在多少个null或空对象，通过isEmpty(Object) 判断元素
Params:
objs – 被检查的对象,一个或者多个
Returns:
存在{@code null}的数量


Objects.deepEquals 可以用来比较数组内容
~~~
  String i1[] = new String[]{"1","2","4"};
        String i2[] = new String[]{"1","2","4"};
        System.out.println(Objects.deepEquals(i1,i2));
~~~

###hutool时间范围
~~~   
 public static void main(String[] args) {
        Date pushTime = DateUtil.parse("2021-11-10 08:00:00");
        if (DateUtil.offsetHour(new Date(), -24).isAfter(pushTime) && DateUtil.offsetHour(new Date(), -48).isBefore(pushTime)) {

            System.out.println(1);
        } else if (DateUtil.offsetHour(new Date(), -48).isAfter(pushTime) && DateUtil.offsetDay(new Date(), -10).isBefore(pushTime)) {
            System.out.println(2);

        } else if (DateUtil.offsetDay(new Date(), -10).isAfter(pushTime)) {
            System.out.println(3);

        }
    }
~~~


###手机号、邮箱等校验
cn.hutool.core.lang.Validator
~~~
            boolean mobile = Validator.isMobile(phone);
            if(!mobile){
                stringBuilder.append("手机号异常");
                jgWarehouseOrder.setCheckState(0);
            }
~~~


###发邮件
~~~
		<dependency>
			<groupId>cn.hutool</groupId>
			<artifactId>hutool-all</artifactId>
			<version>5.7.17</version>
		</dependency>

<dependency>
    <groupId>com.sun.mail</groupId>
    <artifactId>javax.mail</artifactId>
    <version>1.6.2</version>
</dependency>
~~~
mail.setting
~~~
# 发件人（必须正确，否则发送失败）
from = 2542847562@qq.com
# 密码（注意，某些邮箱需要为SMTP服务单独设置授权码，详情查看相关帮助）
pass = xxx
~~~

得到qq邮箱令牌
![image.png](https://upload-images.jianshu.io/upload_images/13965490-954c7e44a7e97348.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


~~~
		MailUtil.send("suoyiguke_yinkai@aliyun.com", "测试", "邮件来自Hutool测试", false);
~~~



###读取classapth下文件
举个例子，假设我们在classpath下放了一个test.xml，读取就变得非常简单：
~~~
String str = ResourceUtil.readUtf8Str("test.xml");
~~~
假设我们的文件存放在src/resources/config目录下，则读取改为：
~~~
String str = ResourceUtil.readUtf8Str("config/test.xml");
~~~
注意 在IDEA中，新加入文件到src/resources目录下，需要重新import项目，以便在编译时顺利把资源文件拷贝到target目录下。如果提示找不到文件，请去target目录下确认文件是否存在。


###字符串

1、format
我会告诉你这是我最引以为豪的方法吗？灵感来自slf4j，可以使用字符串模板代替字符串拼接，我也自己实现了一个，而且变量的标识符都一样，神马叫无缝兼容~~来，上栗子（吃多了上火吧……）

```
String template = "{}爱{}，就像老鼠爱大米";
String str = StrUtil.format(template, "我", "你"); //str -> 我爱你，就像老鼠爱大米
```

参数我定义成了Object类型，如果传别的类型的也可以，会自动调用toString()方法的。

2、StrUtil.cleanBlank 全部情况

###枚举工具类
枚举工具-EnumUtil
cn.hutool.core.util.EnumUtil


###随机工具类
~~~
   // 随机整数（左闭右开）
        int i = RandomUtil.randomInt(1, 100);
        System.out.println("i = " + i);
        // 随机整数（0到边界，左闭右开）
        int j = RandomUtil.randomInt(10);
        System.out.println("j = " + j);
        // 随机字符串
        String str = RandomUtil.randomString(10);
        System.out.println("str = " + str);

        // 随机日期
        DateTime dateTime = RandomUtil.randomDay(1, 10);
        System.out.println("dateTime = " + dateTime);
~~~
