---
title: hutool--唯一ID工具.md
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
title: hutool--唯一ID工具.md
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
唯一ID工具-IdUtil
特别赞助 by：

介绍
在分布式环境中，唯一ID生成应用十分广泛，生成方法也多种多样，Hutool针对一些常用生成策略做了简单封装。

唯一ID生成器的工具类，涵盖了：

UUID
ObjectId（MongoDB）
Snowflake（Twitter）
使用
UUID
UUID全称通用唯一识别码（universally unique identifier），JDK通过java.util.UUID提供了 Leach-Salz 变体的封装。在Hutool中，生成一个UUID字符串方法如下：

//生成的UUID是带-的字符串，类似于：a5c8a5e8-df2b-4706-bea4-08d0939410e3
String uuid = IdUtil.randomUUID();

//生成的是不带-的字符串，类似于：b17f24ff026d40949c85a24f4f375d42
String simpleUUID = IdUtil.simpleUUID();
Copy to clipboardErrorCopied
说明 Hutool重写java.util.UUID的逻辑，对应类为cn.hutool.core.lang.UUID，使生成不带-的UUID字符串不再需要做字符替换，性能提升一倍左右。

ObjectId
ObjectId是MongoDB数据库的一种唯一ID生成策略，是UUID version1的变种，详细介绍可见：服务化框架－分布式Unique ID的生成方法一览。

Hutool针对此封装了cn.hutool.core.lang.ObjectId，快捷创建方法为：

//生成类似：5b9e306a4df4f8c54a39fb0c
String id = ObjectId.next();

//方法2：从Hutool-4.1.14开始提供
String id2 = IdUtil.objectId();
Copy to clipboardErrorCopied
Snowflake
分布式系统中，有一些需要使用全局唯一ID的场景，有些时候我们希望能使用一种简单一些的ID，并且希望ID能够按照时间有序生成。Twitter的Snowflake 算法就是这种生成器。

使用方法如下：

//参数1为终端ID
//参数2为数据中心ID
Snowflake snowflake = IdUtil.getSnowflake(1, 1);
long id = snowflake.nextId();
Copy to clipboardErrorCopied
注意 IdUtil.createSnowflake每次调用会创建一个新的Snowflake对象，不同的Snowflake对象创建的ID可能会有重复，因此请自行维护此对象为单例，或者使用IdUtil.getSnowflake使用全局单例对象。
