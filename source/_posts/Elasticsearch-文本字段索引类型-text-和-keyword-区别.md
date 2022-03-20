---
title: Elasticsearch-文本字段索引类型-text-和-keyword-区别.md
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
title: Elasticsearch-文本字段索引类型-text-和-keyword-区别.md
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
https://www.knowledgedict.com/tutorial/elasticsearch-note.html

es 从 5.0 版本之后，将废弃原来的 string 类型，并将其拆分成两个新的类型 text 类型和 keyword 类型，它们的区别是什么，在何种场景使用？


### 区别

最限制的区别是 text 类型是通过分词用于全文搜索，而 keyword 类型用于关键字的精确匹配，具体区别如下图：

| 类型 | 分词 | 精确查询 | 模糊查询 | 聚合 |
| --- | --- | --- | --- | --- |
| text | 分词后，再索引 | 支持 | 支持 | 不支持 |
| keyword | 不分词索引 | 支持 | 支持 | 支持 |

### 使用

**如果不显性指定字段类型，Elasticsearch 将字符串默认被同时映射成 text 和 keyword 类型**，会自动创建如下的动态映射（dynamic mappings）:

```
      ...
      "question_content": {
        "type": "text",
        "fields":{
          "keyword":{
            "ignore_above":256,
            "type":"keyword"
          }
        }
      },
      ...
```

> 如上，本质上生成了两个字段 question_content 的 text 类型字段和 question_content.keyword 的 keyword 类型字段。

###总结
text 全文检索
~~~
 @Field(type = FieldType.Text,analyzer = "ik_smart",searchAnalyzer = "ik_max_word")//设置为text  可以分词
~~~
keyword 精确检索
