---
title: java-http请求工具之apache的httpclien.md
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
title: java-http请求工具之apache的httpclien.md
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
~~~
    <!-- https://mvnrepository.com/artifact/org.apache.httpcomponents/httpcore -->
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore</artifactId>
      <version>4.4.10</version>
    </dependency>

    <!-- https://mvnrepository.com/artifact/org.apache.httpcomponents/httpclient -->
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpclient</artifactId>
      <version>4.5.6</version>
    </dependency>
~~~

~~~
package com.data.collection.utils;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import org.apache.http.HttpEntity;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.util.EntityUtils;

/**
 * apache http连接池
 */
public class HttpUtils {

    private static CloseableHttpClient httpClient;
    private static RequestConfig requestConfig = RequestConfig.custom()
        .setSocketTimeout(5000)
        .setConnectTimeout(5000)
        .setConnectionRequestTimeout(5000)
        .setMaxRedirects()
        .build();

    static {
        PoolingHttpClientConnectionManager connManager = new PoolingHttpClientConnectionManager();
        connManager.setMaxTotal(300);
        connManager.setDefaultMaxPerRoute(300);
        httpClient = HttpClients.custom().setConnectionManager(connManager).build();
    }

    // get请求
    public static String get(String url) throws IOException {
        HttpGet httpget = new HttpGet(url);
        httpget.setConfig(requestConfig);
        try (CloseableHttpResponse response = httpClient.execute(httpget)) {
            return EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);
        }
    }

    // post请求
    public static String post(String url, String json) throws IOException {
        HttpEntity entity = new StringEntity(json, ContentType.APPLICATION_JSON);
        HttpPost httpPost = new HttpPost(url);
        httpPost.setEntity(entity);
        httpPost.setConfig(requestConfig);
        try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
            return EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);
        }
    }
}
~~~

###三个超时时间

setConnectTimeout：与服务器连接超时时，httpclient会创建一个异步线程用以创建socket连接，此处设置该socket的连接超时时间

setConnectionRequestTimeout：设置从connect Manager获取Connection 超时时间，单位毫秒。这个属性是新加的属性，因为目前版本是可以共享连接池的。

setSocketTimeout：请求获取数据的超时时间，单位毫秒。 如果访问一个接口，多少时间内无法返回数据，就直接放弃此次调用。

###两个连接池大小


.setMaxConnTotal(config.maxConnTotal) ：连接池中最大连接数



                       
.setMaxConnPerRoute(config.maxConnPerRoute)：分配给同一个route(路由)最大的并发连接数。route：运行环境机器 到 目标机器的一条线路。举例来说，我们使用HttpClient的实现来分别请求 www.baidu.com 的资源和 www.bing.com 的资源那么他就会产生两个route。  
