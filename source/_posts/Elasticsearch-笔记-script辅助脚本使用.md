---
title: Elasticsearch-笔记-script辅助脚本使用.md
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
title: Elasticsearch-笔记-script辅助脚本使用.md
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
# es（elasticsearch）如何获取数组字段长度大于某个阈值的文档

![Elasticsearch 笔记](https://upload-images.jianshu.io/upload_images/13965490-8194791abfe23c08.gif?imageMogr2/auto-orient/strip)


es 开发中，如何获取数组字段长度大于某个阈值的文档，可以使用 script 查询。


### Script Query

Elasticsearch 支持使用脚本进行查询，针对过滤数组字段大小在某个阈值以上的文档，可以如下示例：

```
GET product/_search
{
  "query": {
    "script": {
      "script": "doc['menu_id'].values.length > 1"
    }
  }
}
```

