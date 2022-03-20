---
title: 将大list分为包含100元素的小list.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
~~~
	@CacheEvict(value = "HomeDeliveryExtension",key = "#customIds", allEntries = false)
	@Override
	public void saveHomeDeliveryExtension(List<HomeDeliveryExtension> list,String customIds) {
		int listSize = list.size();
		int listNumber = listSize / 2;
		List<List<HomeDeliveryExtension>> allList = ListUtils.partition(list, listNumber==0?1:listNumber);
		for (List<HomeDeliveryExtension> homeDeliveryExtensionList : allList) {
			if (CollectionUtils.isNotEmpty(homeDeliveryExtensionList)) {
				homeDeliveryExtensionDao.saveHomeDeliveryExtension(homeDeliveryExtensionList);
			}
		}
	}
~~~
