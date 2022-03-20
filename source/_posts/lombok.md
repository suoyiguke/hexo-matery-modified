---
title: lombok.md
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
title: lombok.md
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
### `@Builder `注解

~~~
@Data
@Builder
public class CreateSkuDto {
~~~

链式调用构造对象。比传统的set代码要简洁，推荐使用这种方法。三人行必有我师！
~~~
            //-------------------------------------------------封装数据----------
            CreateSkuDto createSkuDto = CreateSkuDto.builder()
                    .itemno(stockProductDetail.getK3Code()) //商品货号  金碟长代码
                    .itemna(stockProduct.getProductName())  //商品名称  迅销商品名称
                    .shname(stockProduct.getProductName())  //商品简称   迅销商品名称
                    //季节代码
                    .branid(stockProduct.getBrandNo())      //品牌代码
                    .cacode(stockProduct.getCatChildNo())//类目代码  三级品类编号
                    .owcode("100")//货主代码
                    .owname("迅销科技股份有限公司")//货主名称
                    //库存承担人代码
                    .itstat(stockProduct.getState() == 0 ? "已上架" : "已下架")//状态
                    //计量类型
                    //商品属性
                    .clientno("100")//货主编码
                    .detail(goodsList)//详情
                    .build();
~~~






###@EqualsAndHashCode 注解
避免手动重写hashCode和eques方法

