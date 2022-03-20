---
title: js-long-精度丢失，在后端使用字符串返回.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: js-long-精度丢失，在后端使用字符串返回.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---

js中无法存储java的long类型。最大值不过 1455799804067174400

![image.png](https://upload-images.jianshu.io/upload_images/13965490-83dfe13a19228017.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以在后端用String代替Long返回

注意jackson的注解和Serializer类的全限定名。这里就算是用错了也不会报错。所以一直不生效
~~~	
/**ID*/
	@com.fasterxml.jackson.databind.annotation.JsonSerialize(using = com.fasterxml.jackson.databind.ser.std.ToStringSerializer.class)
	@com.alibaba.fastjson.annotation.JSONField(serializeUsing= com.alibaba.fastjson.serializer.ToStringSerializer.class)
	private Long id;
~~~
