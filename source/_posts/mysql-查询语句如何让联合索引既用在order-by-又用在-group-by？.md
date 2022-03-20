---
title: mysql-查询语句如何让联合索引既用在order-by-又用在-group-by？.md
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
title: mysql-查询语句如何让联合索引既用在order-by-又用在-group-by？.md
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
思考：如何将idx_user_id_updated_at索引同时使用在order by 和 group by
~~~
EXPLAIN SELECT
	T0.user_id,
	T0.user_name,
	T0.employee_num,
	T0.gender,
	T0.identity_type,
	T0.identity_number,
	T0.mobile,
	T0.email,
	T0.postal_address,
	T0.post_code,
	T0.STATUS,
	T0.job_posts,
	T0.qualification,
	T0.license,
	T0.note,
	T0.ttp_user_oid,
	T0.authentication_mark,
	T0.enabled,
	T0.created_at,
	T0.updated_at,
	GROUP_CONCAT( T2.organization_name ) AS organization_name 
FROM
	biz_user T0
	LEFT JOIN org_user_rel T1 ON T0.user_id = T1.user_id
	LEFT JOIN biz_organization T2 ON T1.org_id = T2.id 
WHERE
	1 = 1 
GROUP BY
	T0.user_id 
ORDER BY
	T0.`updated_at` DESC 
	LIMIT 15
~~~


















**实验现象**

去掉 order by  这样三个Extra都没有出现Using temporary; Using filesort。如果加上order by  T0.`updated_at` DESC  就会出现了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f6ed1b2eb69a8961.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**解决方式**

1、group by 和 order by 都作用于同一个字段。我们可以将id主键设置为自增的int类型。这样就能实现order by date的效果，而且可以同时使用到索引。
~~~
GROUP BY
	T0.user_id 
ORDER BY
	T0.`user_id` DESC 
~~~
2、先在where条件中上到二楼 ：添加条件 WHERE t0.user_id = '11'。这样联合索引中的user_id，updated_at字段就能分别被group by 和 orderby一起使用了！不过这样改sql后就失去本身意义了~

~~~
biz_user T0  force index(idx_user_id_updated_at)
	LEFT JOIN org_user_rel T1 ON T0.user_id = T1.user_id
	LEFT JOIN biz_organization T2 ON T1.org_id = T2.id 
WHERE
	t0.user_id = '11'
GROUP BY
	T0.user_id
ORDER BY
	T0.`updated_at` DESC 
	LIMIT 15
~~~
