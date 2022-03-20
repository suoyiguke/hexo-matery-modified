---
title: 方法2-spring-boot-starter-data-elasticsearch-继承方式一.md
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
title: 方法2-spring-boot-starter-data-elasticsearch-继承方式一.md
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
        <!--es相关-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
        </dependency>

        <dependency>
            <groupId>org.elasticsearch.client</groupId>
            <artifactId>elasticsearch-rest-high-level-client</artifactId>
            <version>7.6.1</version>
        </dependency>


~~~
  # es配置
  elasticsearch:
    rest:
      uris: http://192.168.1.54:9200,http://192.168.1.54:9201
#      uris: http://47.106.191.23:9200
      connection-timeout: 90s
      read-timeout: 90s
~~~





~~~
package com.ruoyi.system.service.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.elasticsearch.domain.vo.MyImg;

public interface MyImgElasticsearchService {


    Boolean insertGoodsToEs(MyImg dto);

    Boolean updateById(MyImg myImg);

    AjaxResult selectMgbGoodsPageForHomePage(Page<MyImg> page, MyImg dto);
}

~~~

~~~
package com.ruoyi.system.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.elasticsearch.domain.vo.MyImg;
import com.ruoyi.system.domain.PageBean;
import com.ruoyi.system.service.MyImgService;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.sort.SortBuilder;
import org.elasticsearch.search.sort.SortBuilders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.ElasticsearchRestTemplate;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.elasticsearch.core.mapping.IndexCoordinates;
import org.springframework.data.elasticsearch.core.query.NativeSearchQuery;
import org.springframework.data.elasticsearch.core.query.NativeSearchQueryBuilder;
import org.springframework.data.elasticsearch.core.query.UpdateQuery;
import org.springframework.data.elasticsearch.core.query.UpdateResponse;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class MMyImgElasticsearchServiceImpl implements MyImgElasticsearchService {
    @Autowired
    private ElasticsearchRestTemplate elasticsearchRestTemplate;
    @Autowired
    private MyImgService myImgService;
    @Autowired
    private ElasticsearchOperations elasticsearchOperations;
    @Override
    public Boolean insertGoodsToEs(MyImg dto) {
        //db
        myImgService.save(dto);
        //es
        MyImg save = elasticsearchRestTemplate.save(dto);
        return save != null;
    }

    @Override
    public Boolean updateById(MyImg myImg) {

        //db
        myImgService.updateById(myImg);

        //es
        Map<String, Object> paramsMap = new HashMap<>(3);
        paramsMap.put("content", myImg.getContent());
        paramsMap.put("title", myImg.getTitle());
        paramsMap.put("url", myImg.getUrl());

        UpdateQuery updateQuery = UpdateQuery.builder(myImg.getId() + "")

            .withScript("ctx._source.content=params.content")
            .withScript("ctx._source.title=params.title")
            .withScript("ctx._source.url=params.url")
            .withParams(paramsMap)
            .build();
        //索引名称
        UpdateResponse img = elasticsearchRestTemplate
            .update(updateQuery, IndexCoordinates.of("img"));
        System.out.println(img);
        return true;
    }


    /**
     * 按标题搜索
     *
     * @param page
     * @param dto
     * @return
     */
    @Override
    public AjaxResult selectMgbGoodsPageForHomePage(Page<MyImg> page, MyImg dto) {
        //搜索条件构造
        //排序
        NativeSearchQueryBuilder queryBuilder = new NativeSearchQueryBuilder();
        //搜索框查询 搜索条件为空查全部
        String title = dto.getTitle();
        if (ObjectUtils.isNotEmpty(title)) {
            queryBuilder.withQuery(QueryBuilders.multiMatchQuery(title,
                "title"));
        } else {
            queryBuilder.withQuery(QueryBuilders.matchAllQuery());
        }

        //排序 默认分数排序
        SortBuilder sortBuilder = getSort();
        queryBuilder.withSort(sortBuilder);
        //分页
        int pageNo = (int) page.getCurrent() - 1;
        queryBuilder.withPageable(PageRequest.of(pageNo, (int) page.getSize()));

        //构造成搜索对象
        NativeSearchQuery query = queryBuilder.build();
        log.info("es:{}", JSONObject.toJSONString(query));
        //执行搜索
        SearchHits<MyImg> search = elasticsearchRestTemplate.search(query, MyImg.class);

        //获取结果
        long totalHits = search.getTotalHits();
        List<MyImg> resultList = new ArrayList<>();
        for (SearchHit<MyImg> searchHit : search.getSearchHits()) {
            MyImg content = searchHit.getContent();
            resultList.add(content);
        }
        //构建分页对象
        PageBean pageBean = new PageBean(page, totalHits, resultList);
        return AjaxResult.success(pageBean);
    }


    /**
     * 功能描述: 排序构建
     *
     * @Param: [dto]
     * @Return: org.elasticsearch.search.sort.SortBuilder
     * @Author: huangjihua
     * @Date: 2021/8/21 18:25
     */
    private SortBuilder getSort() {
        SortBuilder SortBuilder;
        //默认排序为匹配评分排序
        SortBuilder = SortBuilders.scoreSort();
        return SortBuilder;
    }

}

~~~

~~~
package com.ruoyi.elasticsearch.domain.vo;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;
import org.springframework.data.elasticsearch.annotations.Setting;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)

@TableName("my_img")

@Document(indexName = "img", shards = 5, replicas = 1)
@Setting(settingPath = "settings.json")
public class MyImg {

    @TableId(type = IdType.AUTO)
    @Id
    private Long id;
    @Field(type = FieldType.Keyword)
    private String content;
    @Field(type = FieldType.Keyword)
    private String title;
    @Field(type = FieldType.Keyword)
    private String url;

    private Integer pageNo;
    private Integer  pageSize;

}

~~~


controller
~~~
package com.ruoyi.web.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.elasticsearch.domain.vo.MyImg;
import com.ruoyi.system.service.impl.MyImgElasticsearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/es")
public class EsContraller {

    @Autowired
    private MyImgElasticsearchService myImgElasticsearchService;

    @PostMapping("/save")
    public AjaxResult save(@RequestBody MyImg myImg) {
        myImgElasticsearchService.insertGoodsToEs(myImg);
        return AjaxResult.success();
    }

    @PostMapping("/update")
    public AjaxResult update(@RequestBody MyImg myImg) {
        myImgElasticsearchService.updateById(myImg);
        return AjaxResult.success();
    }


    /**
     * 功能描述: 搜索商品信息
     *
     */
    @PostMapping("/list")
    public AjaxResult selectMgbGoodsPage(@RequestBody MyImg dto) {
        Page<MyImg> page = new Page<>(dto.getPageNo(), dto.getPageSize());
        AjaxResult result = myImgElasticsearchService.selectMgbGoodsPageForHomePage(page, dto);
        return result;
    }

}

~~~
