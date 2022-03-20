---
title: java中pojo对象首字母大写导致无法赋值问题.md
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

命名规范(文末附有java命名规范)中指出，属性变量命名应采用**驼峰命名**的方式，即首字母小写，其他单词首字母大写；
但有时候我们对接**三方的接口**时，想要封装实体类来接受，但是发现接收到的参数的变量首字母是大写的或者其他，
**并没有遵循驼峰命名的规范**，这个时候出现的问题就是，用我们封装的对象接收数据时，发现**参数并没有赋上值**。

脑袋大，那么**不符合命名规范的变量**怎么赋值呢。

#### 符合java命名规范的驼峰命名，首字母小写

~~~
 /** * 符合java命名规范的驼峰命名，首字母小写 */
private Integer id; 
public Integer getId() { 
          return id;
} 
public void setId(Integer id) {
      this.id = id;
}
~~~


#### 不符合命名规范的大致分为以下几种情况：
1、首字母大写；
2、 第二个字母大写；
3、 第一、二个字母大写；
4、所有字母都大写

下面是具体每种情况的赋值方式（注意红色标注）

####首字母大写
~~~
/** * 首字母大写 */
    private String UserName; 
     public String getUserName() { 
        return UserName;
    } public void setUserName(String userName) {
        UserName = userName;
    }

~~~
#### 　　第二个字母大写


~~~
    private String pAssword; public String getpAssword() { return pAssword;
    } public void setpAssword(String pAssword) { this.pAssword = pAssword;
    }
~~~


#### 　　第一、二个字母都大写

~~~
/** * 第一、二个字母都大写 */
    private String GEnder; public String getGEnder() { return GEnder;
    } public void setGEnder(String GEnder) { this.GEnder = GEnder;
    }
~~~

#### 　　所有字母都大写
~~~
 /** * 所有字母都大写
     * @return
     */
    private String URL; public String getURL() { return URL;
    } public void setURL(String URL) { this.URL = URL;
    }
~~~


### **java命名规范：**

1、 项目名全部小写

2、 包名全部小写

3、 类名首字母大写，如果类名由多个单词组成，每个单词的首字母都要大写。
　　如：public class MyFirstClass{}
4、 变量名、方法名首字母小写，如果名称由多个单词组成，每个单词的首字母都要大写。
　　如：int index=0;
      　　 public void toString(){}
5、 常量名全部大写
　　如：public static final String GAME_COLOR=”RED”;

6、所有命名规则必须遵循以下规则：
　　1)、名称只能由字母、数字、下划线、$符号组成
　　2)、不能以数字开头
　　3)、名称不能使用JAVA中的关键字。
　　4)、坚决不允许出现中文及拼音命名。

