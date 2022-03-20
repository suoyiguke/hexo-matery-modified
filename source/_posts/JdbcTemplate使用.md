---
title: JdbcTemplate使用.md
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
title: JdbcTemplate使用.md
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
	
###查询list<bean>，封装好直接使用的
~~~
BeanPropertyRowMapper<SignedDataPO> rowMapper = new BeanPropertyRowMapper<SignedDataPO>(SignedDataPO.class);

		List<SignedDataPO> signedDataPOS = jdbcTemplate
			.query("select  * from tlk_signed_data LIMIT 100 ", rowMapper);
~~~

而不是使用queryForList。这里的 Class<T> elementType不能传我们创建的实体类
~~~		
jdbcTemplate.queryForList(sql,SignedDataPO.class);
~~~
