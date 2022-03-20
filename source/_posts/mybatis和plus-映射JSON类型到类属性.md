---
title: mybatis和plus-映射JSON类型到类属性.md
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
title: mybatis和plus-映射JSON类型到类属性.md
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
###mybatis 
写个handel
~~~
@NoArgsConstructor
public class ImagesTypeHandler extends MpJsonTypeHandler{

    public ImagesTypeHandler(Class type) {
        super(Images.class);
    }
}
~~~
接收的实体类

~~~
@Data
public class ZskProdcutDto {
    private List<Images> images;
    private String productName;
}
@Data
public class Images implements Serializable {
    private String id;
    private String type;
    private String orderNum;
    @NotNull(message="图片url，不能为空", groups = {AddGroup.class, UpdateGroup.class})
    private String url;
}

~~~

xml
~~~

    <resultMap id="ZskProdcutMap" type="com.gbm.cloud.treasure.entity.zsk.dto.ZskProdcutDto">
        <id column="images" property="images" typeHandler="com.gbm.cloud.treasure.entity.handler.ImagesTypeHandler"/>
        <id column="product_name" property="productName"/>
    </resultMap>

    <select id="getImage" resultMap="ZskProdcutMap">
        SELECT images,
               concat_ws('/', ifNull(a.product_name, ''), ifNull((SELECT b.customer_goods_name), '')) AS product_name
        FROM stock_product a
                 LEFT JOIN jg_customer_goods_relationship b USING (spu)
        WHERE spu = #{spu}
          AND b.del_status = 0 LIMIT 1;
    </select>

~~~

调用
~~~
                List<ZskProdcutDto> image = ((StockProductRepository) stockProductService.getBaseMapper()).getImage(spu);

~~~

###mybatis_plus
mybatis_plus自动注入的方法需要用注解的方式。

需要设置autoResultMap = true
@TableName(value = "zsk_operation_log",autoResultMap = true)
    /**
     * 修改信息
     */
	@TableField(typeHandler = ZskUpdateInfoTypeHandler.class)
	private List<UpdateInfo> updateInfo;

直接调用BaseService的接口可以生效
