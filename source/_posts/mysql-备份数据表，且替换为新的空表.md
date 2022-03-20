---
title: mysql-备份数据表，且替换为新的空表.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-备份数据表，且替换为新的空表.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
~~~
CREATE TABLE  biz_cloudsign_sign_copy  like biz_cloudsign_sign;
RENAME TABLE biz_cloudsign_sign    TO biz_cloudsign_sign_bak,
             biz_cloudsign_sign_copy    TO biz_cloudsign_sign;
						 
						 
CREATE TABLE  biz_cloudsign_sign_details_copy  like biz_cloudsign_sign_details;
RENAME TABLE biz_cloudsign_sign_details   TO biz_cloudsign_sign_details_bak,
             biz_cloudsign_sign_details_copy    TO biz_cloudsign_sign_details;

~~~
