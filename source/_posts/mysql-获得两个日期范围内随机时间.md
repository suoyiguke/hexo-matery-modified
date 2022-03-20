---
title: mysql-获得两个日期范围内随机时间.md
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
title: mysql-获得两个日期范围内随机时间.md
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
~~~
CREATE DEFINER="root"@"%" FUNCTION "getdate"() RETURNS varchar(255) CHARSET utf8mb4
BEGIN
DECLARE x VARCHAR(255) DEFAULT '';
SET x=  concat(
		CONCAT(
			FLOOR( 2020 + ( RAND( ) * 1 ) ),
			'-',
			LPAD( FLOOR( 9 ), 2, 0 ),
			'-',
			LPAD( FLOOR( 6 + ( RAND( ) * 5 ) ), 2, 0 ) 
		),
		' ',
		CONCAT(
			LPAD( FLOOR( 0 + ( RAND( ) * 23 ) ), 2, 0 ),
			':',
			LPAD( FLOOR( 0 + ( RAND( ) * 59 ) ), 2, 0 ),
			':',
			LPAD( FLOOR( 0 + ( RAND( ) * 59 ) ), 2, 0 ) 
		) ,
		''
	);
RETURN x;
END
~~~
