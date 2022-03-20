---
title: mysql8-0-的-resultset_metadata-调优-提升180%.md
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
title: mysql8-0-的-resultset_metadata-调优-提升180%.md
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
resultset_metadata

System Variable	resultset_metadata
Scope	Session
Dynamic	Yes
SET_VAR Hint Applies	No
Type	Enumeration
Default Value	FULL

###Valid Values	
FULL
NONE

For connections for which metadata transfer is optional, the client sets the resultset_metadata system variable to control whether the server returns result set metadata. Permitted values are FULL (return all metadata; this is the default) and NONE (return no metadata).

For connections that are not metadata-optional, setting resultset_metadata to NONE produces an error.

For details about managing result set metadata transfer, see Optional Result Set Metadata.

~~~
set resultset_metadata = None
~~~


减少mysql返回结果集的大小。提升性能180%

