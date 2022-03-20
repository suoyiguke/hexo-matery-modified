---
title: GuavaCache-源码分析，有效期如何实现得？.md
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
title: GuavaCache-源码分析，有效期如何实现得？.md
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
https://www.cnblogs.com/niejunlei/p/12584773.html


com.google.common.cache.LocalCache#isExpired

~~~

   * Returns true if the entry has expired.
   */
  boolean isExpired(ReferenceEntry<K, V> entry, long now) {
    checkNotNull(entry);
    if (expiresAfterAccess() && (now - entry.getAccessTime() >= expireAfterAccessNanos)) {
      return true;
    }
    if (expiresAfterWrite() && (now - entry.getWriteTime() >= expireAfterWriteNanos)) {
      return true;
    }
    return false;
  }
~~~
