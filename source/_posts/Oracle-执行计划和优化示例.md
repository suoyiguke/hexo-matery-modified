---
title: Oracle-执行计划和优化示例.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
---
title: Oracle-执行计划和优化示例.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
~~~
EXPLAIN PLAN FOR
SELECT
	COUNT( DISTINCT F.CFID ) jg 
FROM
	t_mz_brjbxx T
	INNER  JOIN T_MZ_CFMX F  ON T.MZLSH = F.MZLSH 
WHERE
	F.SJLX = 1 
	AND T.GHSJ BETWEEN  to_date('20190325000000', 'yyyymmddhh24miss')
   and  to_date('20200325235959', 'yyyymmddhh24miss')
	 

SELECT LPAD(' ', LEVEL-1) || OPERATION || ' (' || OPTIONS || ')' "Operation", OBJECT_NAME "Object", OPTIMIZER "Optimizer", COST "Cost", CARDINALITY "Cardinality", BYTES "Bytes", PARTITION_START "Partition Start", PARTITION_ID "Partition ID" , ACCESS_PREDICATES "Access Predicates", FILTER_PREDICATES "Filter Predicates" FROM PLAN_TABLE START WITH ID = 0 CONNECT BY PRIOR ID=PARENT_ID


~~~

###使用exists优化join

使用exists优化join，这种情况exists优势贴别大！ 1.6秒即可。这么快的原因是，exists的子查询更本不需要查询出关联的字段，只需要查出常量即可。
~~~
EXPLAIN PLAN  FOR SELECT COUNT(distinct F.CFID) jg
  FROM T_MZ_CFMX F
 WHERE F.SJLX = 1
   and exists
 (select 'x'
          from t_mz_brjbxx t
         where f.mzlsh = t.mzlsh
           and T.GHSJ between
               to_date('2020-06-01 00:00:00', 'yyyy-mm-dd hh24:mi:ss') and
               to_date('2020-06-30 23:59:59', 'yyyy-mm-dd hh24:mi:ss'))
~~~
使用in看看查询性能如何， 70多秒。垃圾

~~~


 SELECT COUNT(distinct CFID) jg FROM T_MZ_CFMX  WHERE SJLX = 1 AND  mzlsh in (select mzlsh
          from t_mz_brjbxx 
         where 
            GHSJ between
               to_date('2020-06-01 00:00:00', 'yyyy-mm-dd hh24:mi:ss') and
               to_date('2020-06-30 23:59:59', 'yyyy-mm-dd hh24:mi:ss'));

~~~
