---
title: jvm-制造OOM异常.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: jvm-制造OOM异常.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---

###能够导致OutOfMemoryError的代码
先设置
~~~
-Xms10m -Xmx10m -XX:+PrintGCDetails
~~~
执行
~~~
String a = "yinkai";
while (true){
    a += a + new Random().nextInt(88888888)+ new Random().nextInt(999999999);
}
~~~
~~~
int[] arr = new int[1024*1024*1024];
~~~
