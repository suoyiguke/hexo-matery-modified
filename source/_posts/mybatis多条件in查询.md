---
title: mybatis多条件in查询.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis多条件in查询.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
~~~
SELECT * from mgb_undertakes_order WHERE (k3_no,k3_code) in (('6939962112462','6944910310588'))
~~~

换写

~~~

SELECT
	* 
FROM
	mgb_undertakes_order t
WHERE
	EXISTS (
SELECT
	* 
FROM
	mgb_undertakes_order AS t1 
WHERE
	t1.k3_code = t.k3_code 
	AND t1.k3_no = t.k3_no 
	AND t1.k3_code IN ( '6944910310588' ) 
	AND t1.k3_no IN ( '6939962112462') 
	);
~~~


或者 List<Bean> 的形式来做：
~~~
    <select id="embargoRead" resultType="integer" parameterType="com.gbm.cloud.treasure.entity.jg.JgRulaEmbargo">
        select count(*) from jg_rula_embargo where (sku,Province,City,Area) in
        <foreach collection="orderList" item="item" open="(" separator="," close=")">
            (#{item.sku},#{item.Province},#{item.City},#{item.Area})
        </foreach>
    </select>
~~~
