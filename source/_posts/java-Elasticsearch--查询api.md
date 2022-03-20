---
title: java-Elasticsearch--查询api.md
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
title: java-Elasticsearch--查询api.md
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
1、org.elasticsearch.index.query.QueryBuilders#matchQuery 在执行查询时，搜索的词会被分词器分词；再与目标查询字段进行匹配，若分词中的任意一个词与目标字段匹配上，则可查询到。
~~~
//"title" 字段名
queryBuilder.withQuery(QueryBuilders.matchQuery("title",keword));
~~~

2、org.elasticsearch.index.query.QueryBuilders#matchPhraseQuery 不会被分词器分词，而是直接以一个短语的形式查询，而如果你在创建索引所使用的field的value中没有这么一个短语（顺序无差，且连接在一起），那么将查询不出任何结果。


3、org.elasticsearch.index.query.QueryBuilders#multiMatchQuery 多字段的全文搜索，这应该是用的最多的。

~~~
QueryBuilders.multiMatchQuery(keword,"title","content")
~~~
