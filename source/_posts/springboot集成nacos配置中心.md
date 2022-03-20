---
title: springboot集成nacos配置中心.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot集成nacos配置中心.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
###nacos项目主页
https://github.com/alibaba/nacos

###nacos配置启动
使用的nacos版本nacos-server-2.0.0-BETA

1、建立nacos库并导入nacos/conf/nacos-mysql.sql
2、修改配置 nacos/conf/application.properties
~~~
### Count of DB:
db.num=1

### Connect URL of DB:
db.url.0=jdbc:mysql://192.168.1.82:3306/nacos?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&serverTimezone=UTC
db.user.0=root
db.password.0=Sgl20@14

~~~
3、启动 nacos/bin/startup.cmd -m standalone

4、访问 http://localhost:8848/nacos/#/login
账号密码都是 nacos、nacos

5、新增一个配置
配置列表-->点击“+号”新增-->
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5c241fd876221a6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用YAML 格式；dataId 设置为 IAM;

需要剥离的配置内容如下：
~~~
useLocalCache: true
~~~


###sprintboot改动


依赖
~~~
      <!-- nacos-config -->
      <dependency>
        <groupId>com.alibaba.boot</groupId>
        <artifactId>nacos-config-spring-boot-starter</artifactId>
        <version>0.2.7</version>
      </dependency>
~~~

main类；
加上注解:@NacosPropertySource(dataId = "IAM", autoRefreshed = true, type = ConfigType.YAML)；
还有添加监听Nacos加载方法
~~~
package com.ruoyi;

import com.alibaba.nacos.api.config.ConfigType;
import com.alibaba.nacos.api.config.annotation.NacosConfigListener;
import com.alibaba.nacos.spring.context.annotation.config.NacosPropertySource;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

/**
 * 启动程序
 *
 * @author ruoyi
 */
@NacosPropertySource(dataId = "IAM", autoRefreshed = true, type = ConfigType.YAML)
@SpringBootApplication(exclude = {DataSourceAutoConfiguration.class})
public class RuoYiApplication {

    public static void main(String[] args) {
        // System.setProperty("spring.devtools.restart.enabled", "false");
        SpringApplication.run(RuoYiApplication.class, args);
        System.out.println("(♥◠‿◠)ﾉﾞ  若依启动成功   ლ(´ڡ`ლ)ﾞ  \n" +
            " .-------.       ____     __        \n" +
            " |  _ _   \\      \\   \\   /  /    \n" +
            " | ( ' )  |       \\  _. /  '       \n" +
            " |(_ o _) /        _( )_ .'         \n" +
            " | (_,_).' __  ___(_ o _)'          \n" +
            " |  |\\ \\  |  ||   |(_,_)'         \n" +
            " |  | \\ `'   /|   `-'  /           \n" +
            " |  |  \\    /  \\      /           \n" +
            " ''-'   `'-'    `-..-'              ");
    }

    /**
     * 监听Nacos加载
     *
     * @param config
     */
    @NacosConfigListener(dataId = "IAM", type = ConfigType.YAML)
    public void onMessage(String config) {
        System.out.println(config);
    }
}

~~~

springboot集成nacos配置;这个配置和@NacosPropertySource注解选择其一即可，其实是相同的效果
~~~
nacos:
  config:
    server-addr: localhost:8848
    data-id: IAM
~~~



controller里注入useLocalCache; 使用@NacosValue注解而不是原来的@Value
~~~
package com.ruoyi.web.controller.business;

import com.alibaba.nacos.api.config.annotation.NacosValue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import static org.springframework.web.bind.annotation.RequestMethod.GET;

@Controller
@RequestMapping("config")
public class ConfigController {

    private boolean useLocalCache;

    @NacosValue(value = "${useLocalCache}", autoRefreshed = true)
    public void setUseLocalCache(boolean useLocalCache) {
        this.useLocalCache = useLocalCache;
    }

    @RequestMapping(value = "/get", method = GET)
    @ResponseBody
    public boolean get() {
        return useLocalCache;
    }
}
~~~


>注意：用配置中心的配置要把原来的注释掉，不然会一直用默认的

至此集成完毕，现在启动工程会从nacos中拉取上文维护的配置信息


###如何同时指定多个data-id

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1c63a85b0a252eea.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

nacos配置如下
~~~
nacos:
  config:
    type: yaml
    server-addr: 192.168.1.82:8848
    context-path: nacos
    data-ids: IAM,IAM-DATA
    auto-refresh: true
    group: DEFAULT_GROUP
    bootstrap:
      enable: true
      log:
        enable: true
~~~

  dataId之间逗号分割；或者使用多个@NacosPropertySource代替

###其它问题
**nacos启动报错**
1、nacos启动报错ClientOperationServiceProxy.class]: Unsatisfied dependency expressed through constructor parameter 1; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'persistentClien；将data目录删除即可解决；

https://github.com/alibaba/nacos/releases/tag/2.0.0-BETA


**nacos动态刷新配置**
其实大部分的配置在nacos中变更后都可以都到刷新应用，既可以实现不重启springboot服务来达到动态更改的目的；但是像连接像redis、mysql这样使用连接池的数据库是没办法动态刷新的，想要生效就必须重启服务！因为他们的连接参数在程序初始化时就已加载。


**@NacosValue没有读取到配置会报错**
所以得给一个默认值如下：

~~~
    @NacosValue(value = "${business.patientSign.hospital:DEFAULT}", autoRefreshed = true)
    private String hospital;

~~~
而且可以指定默认值常量：
~~~
    @NacosValue(value = "${business.health.url:" + Constants.HEALTHCARDQRCODEDATAURL
        + "}", autoRefreshed = true)
    public void setHealthCardqrCodeDataUrl(String healthCardqrCodeDataUrl) {
        BizPatientSignServiceImpl.healthCardqrCodeDataUrl = healthCardqrCodeDataUrl;
    }
~~~


###Nacos1.4.0启动报错解决方案
看了官网得知Nacos1.4.0环境要求，jdk1.8+ 64，maven3.2.x+。我的操作系统是win10
Caused by: java.lang.UnsatisfiedLinkError: C:\Users\Administrator\AppData\Local\Temp\librocksdbjni6835459412041025213.dll: Can't find dependent 
下载并安装vc++ 2015 依赖库，地址：https://www.microsoft.com/zh-CN/download/details.aspx?id=48145
