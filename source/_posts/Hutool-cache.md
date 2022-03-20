---
title: Hutool-cache.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: Hutool-cache.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---

缓存工具-CacheUtil

###先入先出-FIFOCache  `顺序维度`

~~~

        Cache<String, String> fifoCache = CacheUtil.newFIFOCache(3);

       //加入元素，每个元素可以设置其过期时长，DateUnit.SECOND.getMillis()代表每秒对应的毫秒数，在此为3秒
        fifoCache.put("key1", "value1", DateUnit.SECOND.getMillis() * 3);
        fifoCache.put("key2", "value2", DateUnit.SECOND.getMillis() * 3);
        fifoCache.put("key3", "value3", DateUnit.SECOND.getMillis() * 3);

       //由于缓存容量只有3，当加入第四个元素的时候，根据FIFO规则，最先放入的对象将被移除
        fifoCache.put("key4", "value4", DateUnit.SECOND.getMillis() * 3);

        //value1为null
        String value1 = fifoCache.get("key1");
~~~
###最少使用-LFUCache  `使用次数维度`

~~~
 Cache<String, String> lfuCache = CacheUtil.newLFUCache(3);
        //通过实例化对象创建

        lfuCache.put("key1", "value1", DateUnit.SECOND.getMillis() * 3);
        lfuCache.get("key1");//使用次数+1
        lfuCache.put("key2", "value2", DateUnit.SECOND.getMillis() * 3);
        lfuCache.put("key3", "value3", DateUnit.SECOND.getMillis() * 3);
        lfuCache.put("key4", "value4", DateUnit.SECOND.getMillis() * 3);

        String value2 = lfuCache.get("key2");//null
        String value3 = lfuCache.get("key3");//null
~~~

###最近最久未使用-LRUCache  `空闲时间维度`

~~~
        Cache<String, String> lruCache = CacheUtil.newLRUCache(3);
        lruCache.put("key1", "value1", DateUnit.SECOND.getMillis() * 3);
        lruCache.put("key2", "value2", DateUnit.SECOND.getMillis() * 3);
        lruCache.put("key3", "value3", DateUnit.SECOND.getMillis() * 3);
        lruCache.get("key1");//使用时间推近
        lruCache.put("key4", "value4", DateUnit.SECOND.getMillis() * 3);

        //由于缓存容量只有3，当加入第四个元素的时候，根据LRU规则，最少使用的将被移除（2被移除）
        String value2 = lruCache.get("key");//null
~~~
###超时-TimedCache  `超时时间维度`
~~~
 //创建缓存，默认4毫秒过期
        TimedCache<String, String> timedCache = CacheUtil.newTimedCache(4);

        timedCache.put("key1", "value1", 1);//1毫秒过期
        timedCache.put("key2", "value2", DateUnit.SECOND.getMillis() * 5);
        timedCache.put("key3", "value3");//默认过期(4毫秒)

        //启动定时任务，每5毫秒秒检查一次过期
        timedCache.schedulePrune(5);

        //等待5毫秒
        ThreadUtil.sleep(5);

        //5毫秒后由于value2设置了5毫秒过期，因此只有value2被保留下来
        String value1 = timedCache.get("key1");//null
        String value2 = timedCache.get("key2");//value2

        //5毫秒后，由于设置了默认过期，key3只被保留4毫秒，因此为null
        String value3 = timedCache.get("key3");//null

         //取消定时清理
        timedCache.cancelPruneSchedule();
~~~
>1、如果用户在超时前调用了get(key)方法，会重头计算起始时间。举个例子，用户设置key1的超时时间5s，用户在4s的时候调用了get("key1")，此时超时时间重新计算，再过4s调用get("key1")方法值依旧存在。如果想避开这个机制，请调用get("key1", false)方法。
2、说明 如果启动了定时器，那会定时清理缓存中的过期值，但是如果不起动，那只有在get这个值得时候才检查过期并清理。不起动定时器带来的问题是：有些值如果长时间不访问，会占用缓存的空间。





### 弱引用-WeakCache  `垃圾回收维度`
WeakCache  继承于TimedCache
~~~
        //创建缓存，默认4毫秒过期
        WeakCache<String, String> weakCache = CacheUtil.newWeakCache(DateUnit.SECOND.getMillis() * 3);

        weakCache.put("key1", "value1", 1);//1毫秒过期
        weakCache.put("key2", "value2", DateUnit.SECOND.getMillis() * 5);
        weakCache.put("key3", "value3");//默认过期(4毫秒)

        //启动定时任务，每5毫秒秒检查一次过期
        weakCache.schedulePrune(5);

        //等待5毫秒
        ThreadUtil.sleep(5);

        //5毫秒后由于value2设置了5毫秒过期，因此只有value2被保留下来
        String value1 = weakCache.get("key1");//null
        String value2 = weakCache.get("key2");//value2

        //5毫秒后，由于设置了默认过期，key3只被保留4毫秒，因此为null
        String value3 = weakCache.get("key3");//null

         //取消定时清理
        weakCache.cancelPruneSchedule();
~~~

###文件缓存-FileCache `文件维度`
~~~
        //参数1：容量，能容纳的byte数
        //参数2：最大文件大小，byte数，决定能缓存至少多少文件，大于这个值不被缓存直接读取
        //参数3：超时。毫秒
        LFUFileCache cache = new LFUFileCache(1000, 500, 2000);
        byte[] bytes = cache.getFileBytes("d:/a.jpg");
~~~
