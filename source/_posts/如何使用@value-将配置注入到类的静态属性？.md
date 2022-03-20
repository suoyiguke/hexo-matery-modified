---
title: 如何使用@value-将配置注入到类的静态属性？.md
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
title: 如何使用@value-将配置注入到类的静态属性？.md
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
希望直接将配置文件中的属性注入给某个类的静态属性，这样其他类在使用的时候就不用去获得该类的对象了。
我们可以这样做：使用set注入的方式，将 @Value声明到对应类静态属性的非静态实例set方法上；

注意在目标类上声明@Component注解！将该类纳入apo容器管理，否则@value注入会失败！

请看下面例子：
~~~
package org.jeecg.common.util;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.util.PropertiesUtil;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.Properties;

/**
 * @program: jeecg-boot
 * @description:
 * @author: yinkai
 * @create: 2020-03-27 17:17
 */

@Component
public class WeiXinAppUtil {
    private static String appid;
    private static String secret;
    @Value("${weixinapp.appid}")
    public  void setAppid(String appid) {
        WeiXinAppUtil.appid = appid;
    }
    @Value("${weixinapp.secret}")
    public  void setSecret(String secret) {
        WeiXinAppUtil.secret = secret;
    }
}
~~~

yml中
~~~
weixinapp:
  appid: xxx
  secret:  xxxx
~~~
