---
title: jackson.md
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
title: jackson.md
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
1、忽略指定字段

~~~
@JsonIgnoreProperties({"ordered", "opened"})
public class membershipfee {
}
~~~

经过以上注解的设置，ordered和opened字段将不会转json

也可用
~~~
 @JsonIgnore
~~~

2、忽略内容为空的字段

@JsonIgnoreProperties(ignoreUnknown = true )
public class membershipfee {

}

经过以上设置，内容为null的字段将不再转json

3、时间格式

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private Date loginTime;


~~~
show VARIABLES like '%group_concat_max_len%'
SET GLOBAL group_concat_max_len = 102400;
SET SESSION group_concat_max_len = 102400;
~~~




4、@JsonValue 



@JsonValue 可以用在get方法或者属性字段上，一个类只能用一个，当加上@JsonValue注解是，序列化是只返回这一个字段的值。

例如，实体类中age属性加上注解

    @JsonValue
    private Integer age;

序列化这个类是，只返回了age的值




5、
@JsonSerialize(include= JsonSerialize.Inclusion.ALWAYS)
