---
title: GROUP_CONCAT-多行字段逗号拼接为一行.md
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
title: GROUP_CONCAT-多行字段逗号拼接为一行.md
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
	SELECT
	  GROUP_CONCAT(customer_goods_name)customer_goods_name 
FROM
	`jg_customer_goods_relationship` a 


GROUP_CONCAT(age)
指定分隔符'|'
GROUP_CONCAT(age SEPARATOR '|')
