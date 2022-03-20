---
title: php-定时执行.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: php
categories: php
---
---
title: php-定时执行.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: php
categories: php
---
php没有常驻内存，用户浏览器关闭它也就推出了！我们可以这样自己去调用自己

~~~
<?php

$time = 3;
$url = "http://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
/*
   需要定时执行的方法写到这里
*/

sleep($time);
file_get_contents($url);

~~~

然后在浏览器访问下这个就行了，当然我们可以使用include_once 去执行！
