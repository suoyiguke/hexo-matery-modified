---
title: Value-配合-@PropertySource注入指定配置文件的属性.md
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
title: @Value-配合-@PropertySource注入指定配置文件的属性.md
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
package org.szwj.ca.identityauthsrv.util.common.cache.redis;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;


@Component
@PropertySource(value = {"file:/ias/config/application.properties"})
public class RedisProperty {

    @Value("${spring.redis.enable}")
    private Boolean enable;

    @Value("${spring.redis.host}")
    private String host;

    @Value("${spring.redis.port}")
    private Integer port;

    @Value("${spring.redis.timeout}")
    private Long timeout;

    @Value("${spring.redis.pool.max-idle}")
    private Integer maxIdle;

    @Value("${spring.redis.pool.min-idle}")
    private Integer minIdle;

    @Value("${spring.redis.pool.max-active}")
    private Integer maxActive;

    @Value("${spring.redis.pool.max-wait}")
    private Long maxWait;


    public Boolean getEnable() {
        return enable;
    }

    public String getHost() {
        return host;
    }

    public Integer getPort() {
        return port;
    }

    public Long getTimeout() {
        return timeout;
    }

    public Integer getMaxIdle() {
        return maxIdle;
    }

    public Integer getMinIdle() {
        return minIdle;
    }

    public Integer getMaxActive() {
        return maxActive;
    }

    public Long getMaxWait() {
        return maxWait;
    }
}


~~~
