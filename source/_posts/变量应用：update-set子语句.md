---
title: 变量应用：update-set子语句.md
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
title: 变量应用：update-set子语句.md
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

SELECT uuid into @x FROM mgb_dict_data WHERE dict_label = '物流问题'

UPDATE mgb_dict_data 
SET parent_uuid = ( @x ) 
WHERE
	dict_label IN ( '责任判定', '物流损坏', '物流丢件', '物流退件', '配送问题', '物流管制')
