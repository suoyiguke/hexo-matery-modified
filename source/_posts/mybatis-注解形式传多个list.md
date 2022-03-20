---
title: mybatis-注解形式传多个list.md
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
title: mybatis-注解形式传多个list.md
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
~~~
    @Select("<script>"+
            "SELECT\n" +
            "	  concat(b.k3_code,',',b.bar_code) k3CodeK3No ,a.supplier_no supplierNo,a.spu,b.id detailId ,b.first_tag firstTag,a.product_name productName,(SELECT brand_name from  product_brand  s WHERE s.brand_no = a.brand_no) brandName " +
            "FROM\n" +
            "	stock_product a\n" +
            "	JOIN stock_product_detail b ON a.spu = b.spu \n" +
            "WHERE\n" +
            " b.k3_code IN  \n" +
            "<foreach collection='k3CodeList' item='id' open='(' separator=',' close=')'>" +
            "#{id}" +
            "</foreach>" +
            "	AND b.bar_code IN \n" +
            "<foreach collection='k3NoList' item='id' open='(' separator=',' close=')'>" +
            "#{id}" +
            "</foreach> " +
            "</script>"+
            "	")
    List<Map> getSupplierNoByk3Code(@Param("k3CodeList")  List<String> k3CodeList,@Param("k3NoList")  List<String> k3NoList);
~~~
