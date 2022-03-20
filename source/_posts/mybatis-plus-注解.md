---
title: mybatis-plus-注解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis-plus-注解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
1、@TableId(type = IdType.AUTO) 数据库自增

2、插入为null也插入，默认为null就会忽略这个字段
	@TableField(insertStrategy = FieldStrategy.IGNORED )


3、修改为null也修改
@TableField(updateStrategy = FieldStrategy.IGNORED )
如果null有具体业务含义，那么必须加上这个注解

4、对应mysql json 类型
~~~
@TableName(value="jq_return_exchange",autoResultMap = true)
    /**
     * 客服备注
     */
    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<Map<String,Object>> remark;
~~~
如果是自定义实体类，就也要写自定义handel
~~~
    /**
     * 规格
     */
    @TableField(typeHandler = ProductDetailSpecTypeHandler.class)
    private List<StockProductDetailSpec> specData;
package com.gbm.cloud.treasure.entity.handler;

import com.gbm.cloud.treasure.entity.product.ProductDetailSpec;

public class ProductDetailSpecTypeHandler extends MpJsonTypeHandler{

    public ProductDetailSpecTypeHandler(Class type) {
        super(ProductDetailSpec.class);
    }

    public ProductDetailSpecTypeHandler() {
        super();
    }
}

~~~




5、	时间格式化
~~~
    @com.fasterxml.jackson.annotation.JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd HH:mm:ss")
    @org.springframework.format.annotation.DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @com.alibaba.excel.annotation.format.DateTimeFormat("yyyy-MM-dd HH:mm:ss")
~~~



6、DTO包装类使用注解自动配置resultMap
@TableName(autoResultMap = true) 这种方式可以直接代替mybatis的@result注解
~~~
package com.gbm.cloud.treasure.entity.mgbUndertakesOrder;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName(autoResultMap = true)
public class OrderInfoDto {
    private Long id;
    private String spu;
    private String sku;
    private String model;

    @TableField("is_combination")
    private Integer isCombination;
    @TableField("supplier_no")
    private String supplierNo;
    @TableField("product_name")
    private String productName;
    @TableField("supplier_name")
    private String supplierName;
    @TableField("cat_name")
    private String catName;
    @TableField("k3_code")
    private String k3Code;
    @TableField("spec_data")
    private String specData;
    @TableField("bar_code")
    private String barCode;
}

~~~

~~~
    @Select({
            "<script>",
            "SELECT",
            "	a.spu,",
            "   a.is_combination,",
            "	a.supplier_no,",
            "	a.product_name,",
            "	( SELECT supplier_name FROM supplier WHERE supplier_no = a.supplier_no LIMIT 1 ) supplier_name,",
            "	( SELECT cat_name FROM `product_category` WHERE cat_no = a.cat_root_no LIMIT 1 ) cat_name,",
            "	b.id,",
            "   b.sku,",
            "	b.k3_code,",
            "	b.spec_data,",
            "	b.bar_code,",
            "	b.model",
            "FROM",
            "	stock_product a",
            "	JOIN stock_product_detail b USING ( spu ) ",
            "WHERE",
            "	b.sku IN",
            "<foreach collection='skuList' item='sku' open='(' separator=',' close=')'>",
            "#{sku}",
            "</foreach>",
            "</script>"
    })
    List<OrderInfoDto> getOrderOtherInfoBySKUList1(@Param("skuList") Collection<String> skuList);
~~~


7、逻辑删除注解，配置上后所有的select自己会加del_status=0
    /**
     * 删除状态（0：启用 1：禁用）
     */
    @TableField("del_status")
    @TableLogic(value = "0",delval = "1")
    private Integer delStatus;

