---
title: java文件基本操作.md
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
title: java文件基本操作.md
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


1、file 转 byte[]
    File file = new File("D:\\111.jpg");
        byte[] bytes = FileUtils.readFileToByteArray(file);

2、inputstrem转字节数组，使用IOutils
~~~
IOUtils.toByteArray(inputStream))
~~~
