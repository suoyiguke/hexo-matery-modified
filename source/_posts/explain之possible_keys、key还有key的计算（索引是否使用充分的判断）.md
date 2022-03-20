---
title: explain之possible_keys、key还有key的计算（索引是否使用充分的判断）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: explain之possible_keys、key还有key的计算（索引是否使用充分的判断）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
### possible_keys列

该列表示可能的索引选择。

请注意，此列完全独立于表的顺序，这就意味着possible_keys在实践中，某些键可能无法与生成的表顺序一起使用。

![图片](https://upload-images.jianshu.io/upload_images/13965490-177563f5a0bd37c5?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果此列是NULL，则没有相关的索引。在这种情况下，您可以通过检查该WHERE 子句以检查它是否引用了某些适合索引的列，从而提高查询性能。

### key列

该列表示实际用到的索引。

可能会出现possible_keys列为NULL，但是key不为NULL的情况。

演示之前，先看看test1表结构：

![图片](https://upload-images.jianshu.io/upload_images/13965490-d20d31e7dc4a1011?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

test1表中数据： 

![图片](https://upload-images.jianshu.io/upload_images/13965490-595eff236b427304?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用的索引：

![图片](https://upload-images.jianshu.io/upload_images/13965490-01ce59f8ae2d1974?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

code和name字段使用了联合索引。

执行sql如下：

```
explain select code  from test1;
```

结果：

![图片](https://upload-images.jianshu.io/upload_images/13965490-7073d2c10fa29891?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这条sql预计没有使用索引，但是实际上使用了全索引扫描方式的索引。

### key_len列

该列表示使用索引的长度。上面的key列可以看出有没有使用索引，key_len列则可以更进一步看出索引使用是否充分。不出意外的话，它是最重要的列。

![图片](https://upload-images.jianshu.io/upload_images/13965490-5aad12bf80a9ffa7?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**有个关键的问题浮出水面：key_len是如何计算的？**

决定key_len值的三个因素：

  1.字符集

  2.长度

  3.是否为空 

常用的字符编码占用字节数量如下：

![图片](https://upload-images.jianshu.io/upload_images/13965490-c766dba3c0759602?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

目前我的数据库字符编码格式用的：UTF8占3个字节。

mysql常用字段占用字节数：

| 字段类型 | 占用字节数 |
| --- | --- |
| char(n) | n |
| varchar(n) |  n + 2 |
| tinyint | 1 |
| smallint | 2 |
| int | 4 |
| bigint | 8 |
| date | 3 |
| timestamp | 4 |
| datetime | 8 |

### 此外，如果字段类型允许为空则加1个字节。

### 上图中的 184是怎么算的？

### 184 = 30 * 3 + 2 + 30 * 3 + 2

  再把test1表的code字段类型改成char，并且改成允许为空：

![图片](https://upload-images.jianshu.io/upload_images/13965490-2ef718ff3a0793a6?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

执行sql如下：

```
explain select code  from test1;
```

### 结果：

![图片](https://upload-images.jianshu.io/upload_images/13965490-0e7e60cbb4ba7c52?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 怎么算的？

183 = 30 * 3 + 1 + 30 * 3 + 2

**还有一个问题：为什么这列表示索引使用是否充分呢，还有使用不充分的情况？** 

执行sql如下：

```
explain select code  from test1 where code='001';
```

### 结果：

![图片](https://upload-images.jianshu.io/upload_images/13965490-039b95f000e5454e?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

上图中使用了联合索引：idx_code_name，如果索引全匹配key_len应该是183，但实际上却是92，这就说明没有使用所有的索引，索引使用不充分。
