---
title: org-apache-commons-lang3-StringUtils.md
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
title: org-apache-commons-lang3-StringUtils.md
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
###equalsAny
                    if(StringUtils.equalsAny(clientPrintTemplate.getSystemTemplateId(),"HW150",SfTemplateRelationType.SF150.getSyCode())){



###defaultIfBlank
~~~
    organizationName = StringUtils
                    .defaultIfBlank(propertiesMap.get("cloudsign.organizationName"),
                        Constants.DEFAULT_ORGANIZATIONNAME);

~~~

###isBlank

###isAllBlank 批量变量非空判断，全部为空返回true
~~~
boolean allBlank = StringUtils.isAllBlank("", null, "  ");
System.out.println(allBlank);//true

boolean allBlank = StringUtils.isAllBlank("", null, "  ","123");
System.out.println(allBlank);//false
~~~
### isAnyBlank 任何一个为空返回true （平时使用参数非空校验可以使用它）
~~~
boolean allBlank = StringUtils.isAnyBlank("", null, "  ","123");
System.out.println(allBlank);//true
~~~


###remove  从字符中去掉指定子字符串

~~~
String remove = StringUtils.remove("yinkai", "kai");
System.out.println(remove);
~~~


1、截取指定字符之前的字符串
org.apache.commons.lang.StringUtils#substringBefore

2、如果不存在就拼接前缀
cn.hutool.core.text.CharSequenceUtil#addPrefixIfNot
