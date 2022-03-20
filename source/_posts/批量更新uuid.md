---
title: 批量更新uuid.md
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
title: 批量更新uuid.md
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
1、批量更新uuid
UPDATE mgb_dict_data SET uuid=UUID();

UPDATE mgb_dict_data SET uuid=REPLACE(uuid, '-', '');

注意不能使用UPDATE honghang_1month_list SET id=REPLACE(UUID(), '-', '');  要分开执行。

 2、批量更新自增id
SET @rownum = 0;
UPDATE `mgb_dict_data` 
SET dict_value = ( SELECT @rownum := @rownum + 1 AS nid ) 
WHERE
	dict_type = 'liability_judgment_type';
