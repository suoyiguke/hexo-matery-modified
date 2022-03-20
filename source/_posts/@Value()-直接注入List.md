---
title: Value()-直接注入List.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: @Value()-直接注入List.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
~~~
	/**
	 * Some urls with suffixes which needn't auth, such as htm, html, js and so on.
	 */
	@Value("#{'${auth.filter.exclude-url-suffixes}'.split(',')}")
	private List<String> authFilterExcludeUrlSuffixes;
~~~
