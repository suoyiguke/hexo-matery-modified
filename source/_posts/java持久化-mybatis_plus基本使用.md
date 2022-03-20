---
title: java持久化-mybatis_plus基本使用.md
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
title: java持久化-mybatis_plus基本使用.md
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

官网 https://mp.baomidou.com/

###QueryWrapper的使用

1、	QueryWrapper<SysDepart> queryWrapper = new QueryWrapper<>();
		queryWrapper.in("id",id).select("org_code orgCode");
		List<Object> objects = departMapper.selectObjs(queryWrapper);


2、QueryWrapper和自定义mapper结合使用

mapper
~~~
    @Select("SELECT * FROM product_after_sale_terms ${ew.customSqlSegment}")
    IPage<AfterSaleTermsDto> findByPage(@Param("page") IPage<AfterSaleTermsDto> page, @Param(Constants.WRAPPER) Wrapper<AfterSaleTermsDto> queryWrapper);

~~~

使用
~~~
    QueryWrapper<AfterSaleTermsDto> wrapper = new QueryWrapper();
        if (columnMap.get("state")!=null){
            wrapper.eq("state",Integer.parseInt(columnMap.get("state")+""));
        }
        IPage<AfterSaleTermsDto> page =afterSaleTermsRepository.findByPage(new MyBatisPlusPageUtil<AfterSaleTermsDto>().getPage(columnMap), wrapper);
~~~
