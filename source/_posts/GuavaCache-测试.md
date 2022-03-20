---
title: GuavaCache-测试.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-GuavaCache
categories: java-GuavaCache
---
---
title: GuavaCache-测试.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-GuavaCache
categories: java-GuavaCache
---
1、GuavaCache 的失效时间是 Cache对象的属性

![image.png](https://upload-images.jianshu.io/upload_images/13965490-6d6764f1b4cf4f8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


如下构造Cache 
~~~
    protected Cache createGuavaCache(String name, CacheBuilder builder, long duration,
        TimeUnit unit) {

        com.google.common.cache.Cache<Object, Object> cache = null;
        if (builder == null) {
            cache = CacheBuilder.newBuilder()
                .expireAfterAccess(duration, unit)  //数据如果在30分钟内,没有被访问则会被移除
                .expireAfterWrite(duration, unit)   //数据写入30分钟后会被自动移除
                .concurrencyLevel(10)               //Map结构的对象支持最多10个调用方同时更新这个缓存结构的数据,即并发更新操作最大数量为10.
                .initialCapacity(20)                //初始大小为20(能存20个键值对),
                .maximumSize(500)                   //设置缓存最大容量为500，超过500之后就会按照LRU最近虽少使用算法来移除缓存项
                .softValues()
                .build();
        } else {
            cache = builder.build();
        }
        return new GuavaCache(name, cache, isAllowNullValues());

    }

~~~

2、证明 GuavaCache 的失效时间是和redis一样对 每个key都有独立的时间的代码。

~~~
	@Autowired
	CacheUtils cacheUtils;
	@Test
	public void contextLoads() throws InterruptedException {
		cacheUtils.addPointName("zzz","key1","yinkai",20, TimeUnit.SECONDS);

		TimeUnit.SECONDS.sleep(10);
		cacheUtils.addPointName("zzz","key2","ffffff",20, TimeUnit.SECONDS);
		TimeUnit.SECONDS.sleep(12);

		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key1"));
		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key2"));


	}

~~~
最终输出，key1 缓存没有因为key2的插入而刷新！也就是说一个Cache中虽然是指定所有key的失效时间。但是并不是每个key都会使用同一套的失效时间，也就是说：每个key都有独立的时间！
~~~

ffffff
~~~


或者可以这样，更加直观地验证这个结论
~~~
	cacheUtils.addPointName("zzz","key1","yinkai",10, TimeUnit.SECONDS);

		TimeUnit.SECONDS.sleep(5);
		cacheUtils.addPointName("zzz","key2","ffffff",10, TimeUnit.SECONDS);

		while (true){
			System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key1"));
			System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key2"));

		}
~~~

3、GuavaCache 刷新失效时间，顺延失效时间。再次写入可以做到

~~~
	@Autowired
	CacheUtils cacheUtils;
	@Test
	public void contextLoads() throws InterruptedException {
               //1
		cacheUtils.addPointName("zzz","key1","yinkai",20, TimeUnit.SECONDS);

		TimeUnit.SECONDS.sleep(10);
                 //2
		cacheUtils.addPointName("zzz","key1","yinkai",20, TimeUnit.SECONDS);
		cacheUtils.addPointName("zzz","key2","ffffff",20, TimeUnit.SECONDS);
		TimeUnit.SECONDS.sleep(12);
		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key1"));
		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key2"));


	}
~~~

4、在失效之前读取不能刷新时间

~~~
		cacheUtils.addPointName("zzz","key1","yinkai",20, TimeUnit.SECONDS);

		TimeUnit.SECONDS.sleep(10);
		//失效之前读取key1
		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key1"));
		cacheUtils.addPointName("zzz","key2","ffffff",20, TimeUnit.SECONDS);
		TimeUnit.SECONDS.sleep(12);
		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key1"));
		System.out.println(cacheUtils.getValueByPointNameAndKey("zzz","key2"));
~~~

输出
~~~
yinkai
2020-07-14 09:35:41,480 [main] INFO  o.s.c.i.util.common.cache.guava.GuavaCache:101 - 存入缓存key==key2,存入对象="ffffff"

ffffff
~~~



5、GuavaCache  使用单例模式构造cache对象。保证一个cachename对应一个Cache对象
~~~
  public Cache getCache(String name,long duration, TimeUnit unit) {

        Cache cache = this.cacheMap.get(name);
        if (cache == null && this.dynamic) {
            synchronized (this.cacheMap) {
                cache = this.cacheMap.get(name);
                if (cache == null) {
                    CacheBuilder builder = this.builderMap.get(name);
                    cache = createGuavaCache(name, builder, duration, unit);
                    this.cacheMap.put(name, cache);
                }
            }
        }
        return cache;

    }
~~~

这样得话，这个addPointName方法在第一次调用时就已经决定这个cache对象得失效时间了。第二次再调用是不会更改这个失效时间。
~~~
    /**
     * cache指定name
     * @param name
     */
    public void addPointName(String name, String key, Object value, long time, TimeUnit timeUnit) {
        if (!redisProperty.getEnable()) {
            Cache cache = guavaCacheManager.getCache(name,time,timeUnit);
            cache.put(key, value);
        } else {
            redisUtils.Add(key, value, time, timeUnit);
        }
    }
~~~
