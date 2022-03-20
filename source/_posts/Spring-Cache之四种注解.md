---
title: Spring-Cache之四种注解.md
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
title: Spring-Cache之四种注解.md
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
###@Cacheable

~~~
	@Cacheable(value = "HomeDeliveryExtension",key = "#customIds")
	@Override
	public List<HomeDeliveryExtension> getHomeDeliveryExtension(List<String> customIdList,String customIds) {
		return homeDeliveryExtensionDao.getHomeDeliveryExtension(customIdList);
	}
~~~
>在redis中保存形式：key = HomeDeliveryExtension:66666 ， value=xxxxx

###@CacheEvict	
将一条或多条数据从缓存中删除
~~~
	@CacheEvict(value = "HomeDeliveryExtension",key = "#customIds", allEntries = false)
	@Override
	public void saveHomeDeliveryExtension( List<HomeDeliveryExtension> list,String customIds) {
		if (CollectionUtils.isNotEmpty(list)) {
			homeDeliveryExtensionDao.saveHomeDeliveryExtension(list);
		}
	}
~~~

>allEntries =ture ，会忽略key的值。直接清除掉所有"HomeDeliveryExtension"的缓存
allEntries =false，针对value和key清理

###@CachePut

@CachePut	无论怎样，都会将方法的返回值放到缓存中。

###@Caching	
@Caching注解可以让我们在一个方法或者类上同时指定多个Spring Cache相关的注解。其拥有三个属性：cacheable、put和evict，分别用于指定@Cacheable、@CachePut和@CacheEvict。

~~~
	@Caching(cacheable = @Cacheable("users"), 
			evict = { @CacheEvict("cache2"),
					@CacheEvict(value = "cache3", allEntries = true) })
~~~




###多个参数怎么写key？
字符串拼接
~~~
@Autowired
	private ICustomQueryConfigDao customQueryConfigDao;

	@Cacheable(value = "CustomQueryConfig",key = "'('+#memberNo+','+#pageName+')'")
	@Override
	public String getOrderQueryConifg(Long memberNo, String pageName) {
		return customQueryConfigDao.getOrderQueryConifg(memberNo,pageName);
	}

	@CacheEvict(value = "CustomQueryConfig",key = "'('+#memberNo+','+#pageName+')'")
	@Override
	public void saveQueryConifg(Long memberNo, String pageName,String value) {
		customQueryConfigDao.saveQueryConifg(memberNo,pageName,value);
	}
~~~
