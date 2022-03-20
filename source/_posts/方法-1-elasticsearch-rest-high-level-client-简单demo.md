---
title: 方法-1-elasticsearch-rest-high-level-client-简单demo.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
---
title: 方法-1-elasticsearch-rest-high-level-client-简单demo.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 全文搜索
categories: 全文搜索
---
~~~
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <parent>
    <artifactId>ruoyi</artifactId>
    <groupId>com.ruoyi</groupId>
    <version>3.7.0</version>
  </parent>
  <modelVersion>4.0.0</modelVersion>

  <artifactId>elasticsearch</artifactId>

  <dependencies>
    <!-- 通用工具-->
    <dependency>
      <groupId>com.ruoyi</groupId>
      <artifactId>ruoyi-common</artifactId>
    </dependency>
    <!-- spring-boot-devtools -->
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-devtools</artifactId>
      <optional>true</optional> <!-- 表示依赖不会传递 -->
    </dependency>

    <dependency>
      <groupId>org.elasticsearch.client</groupId>
      <artifactId>elasticsearch-rest-high-level-client</artifactId>
      <version>7.17.0</version>
    </dependency>
    <dependency>
      <groupId>org.elasticsearch.client</groupId>
      <artifactId>elasticsearch-rest-client</artifactId>
      <version>7.17.0</version>
    </dependency>
    <dependency>
      <groupId>org.elasticsearch</groupId>
      <artifactId>elasticsearch</artifactId>
      <version>7.17.0</version>
    </dependency>
    <!--springboot的测试框架,里面有对junit4的依赖-->
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>

    <!--Lombok-->
    <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <scope>provided</scope>
    </dependency>
    <!--测试依赖-->
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <scope>test</scope>
    </dependency>

  </dependencies>

</project>
~~~
~~~
package com.ruoyi;

import com.alibaba.fastjson.JSONObject;
import com.ruoyi.elasticsearch.domain.MyImg;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.http.HttpHost;
import org.elasticsearch.action.DocWriteRequest;
import org.elasticsearch.action.bulk.BulkItemResponse;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.bulk.BulkResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.client.core.CountRequest;
import org.elasticsearch.client.core.CountResponse;
import org.elasticsearch.index.query.BoolQueryBuilder;
import org.elasticsearch.index.query.MatchAllQueryBuilder;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.xcontent.XContentType;
import org.junit.Before;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@Slf4j
@Configurable
@SpringBootApplication
public class MainApplication {

    RestHighLevelClient restHighLevelClient;
    RestClientBuilder localhost;

    @Before
    public void init() {
        //创建低级客户端,提供ip,端口,设置超时重试时间
        localhost = RestClient.builder(new HttpHost("localhost", 9200));
        //创建高级客户端,传入低级客户端
        restHighLevelClient = new RestHighLevelClient(localhost);
    }


    @Test
    public void query() throws IOException {
        SearchRequest searchRequest = new SearchRequest("db").types("img");
        QueryBuilder queryBuilder = new MatchAllQueryBuilder();
        SearchSourceBuilder builder = new SearchSourceBuilder().query(queryBuilder).size(10);
        //请求对象携带条件,查询类型,一般默认即可
        searchRequest.source(builder).searchType(SearchType.DEFAULT);
        try {

            //通过高级客户端执行查询请求,返回响应对象
            SearchResponse searchResponse = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
            //拿到响应的匹配结果,遍历
            for (SearchHit hit : searchResponse.getHits().getHits()) {
                //转为String,也可以getSourceAsMap转为map,后续进行操作
                System.out.println(hit.getSourceAsString());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    @Test
    public void add() throws IOException {
        BulkRequest bulkRequest = new BulkRequest();
        ArrayList<MyImg> list = new ArrayList<>();
        list.add(new MyImg().setId(1L).setContent("yinkai").setTitle("good programer"));
        //批量数据
        //下面尽量控制一下一次bulk的数量，如果数据过大，条数过多可能出现同步不完全的情况
        //转为map,这里根据自己的使用习惯来转map，我这里是通过反射自定义的方法
        Map<Long, MyImg> map = list.stream()
            .collect(Collectors.toMap(MyImg::getId, Function.identity()));
        bulkRequest.add(new IndexRequest("db", "img")
            .source(map, XContentType.JSON));
        try {
            BulkResponse response = restHighLevelClient.bulk(bulkRequest, RequestOptions.DEFAULT);
            if (response.hasFailures()) {
                exceptionRetry(bulkRequest, response);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 异常捕获用于重试
     */
    private void exceptionRetry(BulkRequest request, BulkResponse response) {
        List<DocWriteRequest<?>> list = request.requests();
        BulkRequest requestRetry = new BulkRequest();
        //下面尽量控制一下一次bulk的数量，如果数据过大，条数过多可能出现同步不完全的情况
        for (BulkItemResponse bir : response) {
            if (bir.isFailed()) {
                int docIndex = bir.getItemId();
                IndexRequest ir = (IndexRequest) list.get(docIndex);
                requestRetry
                    .add(new IndexRequest("db", "img")
                        .source(ir.sourceAsMap(), XContentType.JSON));
            }
        }
        try {
            //遇到错误，休眠1s后重试
            Thread.sleep(1000);
            BulkResponse responseRetry = restHighLevelClient
                .bulk(requestRetry, RequestOptions.DEFAULT);
        } catch (Exception e) {
        }
    }


    /**************************************count查询***************************************/
    public long count(String indexName, MyImg demo) {
        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();
        //构建判断条件
        BoolQueryBuilder boolBuilder = makeQueryParams(demo);
        sourceBuilder.query(boolBuilder);
        CountRequest countRequest = new CountRequest(indexName);
        countRequest.source(sourceBuilder);
        CountResponse countResponse;
        long count = 0L;
        try {
            countResponse = restHighLevelClient.count(countRequest, RequestOptions.DEFAULT);
            count = countResponse != null ? countResponse.getCount() : 0;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return count;
    }

    /*****************************构建查询参数****************************************/
//构建查询参数
    private static BoolQueryBuilder makeQueryParams(MyImg demo) {

        BoolQueryBuilder boolQueryBuilder = new BoolQueryBuilder();
        //精确查找
        if (demo.getId() != null) {
            boolQueryBuilder.must(QueryBuilders.termQuery("id", String.valueOf(demo.getId())));
        }
//        //范围匹配
//        if (!StringUtils.isEmpty(demo.getCreateDate())) {
//            boolQueryBuilder.must(rangeQuery("createDate").gte(demo.getCreateDate()).format("yyyy-MM-dd"));
//        }
        //模糊匹配
//        if (!StringUtils.isEmpty(demo.getTitle())) {
//            boolQueryBuilder
//                .must(QueryBuilders.wildcardQuery("title", String.format("*%s*", demo.getTitle())));
//        }
        return boolQueryBuilder;
    }

    /**************************************分页条件查询***************************************/
    @Test
    public void getListFromEs() {
        //创建低级客户端,提供ip,端口,设置超时重试时间
        localhost = RestClient.builder(new HttpHost("localhost", 9200));
        //创建高级客户端,传入低级客户端
        restHighLevelClient = new RestHighLevelClient(localhost);
        MyImg MyImg = new MyImg().setId(1L).setTitle("x");

        SearchRequest request = new SearchRequest("db").types("img");
        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();
        sourceBuilder.query(makeQueryParams(MyImg));//查询参数
        sourceBuilder.size(100);
//        sourceBuilder.from(0).size(100);//分页
//        sourceBuilder.sort("id", SortOrder.DESC);//排序字段
        request.source(sourceBuilder);

        SearchHit[] hits = new SearchHit[0];
        try {
            hits = restHighLevelClient.search(request, RequestOptions.DEFAULT).getHits().getHits();
        } catch (Exception e) {
            log.error("ES查询出错: {}", e.getMessage(), e);
        }

        List<MyImg> data = Arrays.stream(hits)
            .collect(Collectors.mapping(
                hit -> JSONObject.parseObject(hit.getSourceAsString(), MyImg.class),
                Collectors.toList()));

        data.forEach(o -> {
            System.out.println(o);
        });
    }
}
~~~


~~~
package com.ruoyi.elasticsearch.domain;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)
public class MyImg {
    @Id
    private Long id;
    private String content;
    private String title;
    private String url;
}

~~~
