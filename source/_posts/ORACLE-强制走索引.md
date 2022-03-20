---
title: ORACLE-强制走索引.md
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
title: ORACLE-强制走索引.md
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
	  /*+index(F Relationship_5_FK) index(T SQ_BRJBXX_GHSJ)*/ COUNT( DISTINCT F.CFID ) jg 
FROM
	t_mz_brjbxx T
	INNER  JOIN T_MZ_CFMX F  ON T.MZLSH = F.MZLSH 
WHERE
	F.SJLX = 1 
	AND T.GHSJ BETWEEN  to_date('20190325000000', 'yyyymmddhh24miss')
   and  to_date('20200325235959', 'yyyymmddhh24miss')
~~~ 
