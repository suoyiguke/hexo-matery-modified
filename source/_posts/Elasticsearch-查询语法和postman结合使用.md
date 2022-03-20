---
title: Elasticsearch-查询语法和postman结合使用.md
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
title: Elasticsearch-查询语法和postman结合使用.md
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
###Get 查看所有索引
~~~
http://localhost:9200/_all
~~~

结果：如下img、db、person、recipes都是我建立的索引
~~~
{
    ".apm-agent-configuration":Object{...},
    ".apm-custom-link":Object{...},
    ".kibana_7.17.0_001":Object{...},
    ".kibana_task_manager_7.17.0_001":Object{...},
    ".tasks":Object{...},
    "db":Object{...},
    "img":Object{...},
    "person":Object{...},
    "recipes":Object{...}
}
~~~
打开recipes看下它的字段和字段数据类型
~~~
   "recipes":{
        "aliases":Object{...},
        "mappings":{
            "properties":{
                "name":{
                    "type":"text",
                    "fields":{
                        "keyword":{
                            "type":"keyword",
                            "ignore_above":256
                        }
                    }
                },
                "rating":Object{...},
                "type":Object{...}
            }
        },
        "settings":Object{...}
    }
~~~


###查看指定索引的mapping数据类型
~~~
GET http://localhost:9200/recipes/_mapping
return
{
    "recipes": {
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "rating": {
                    "type": "long"
                },
                "type": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }
            }
        }
    }
}
~~~


###PUT 创建索引
~~~
http://localhost:9200/recipes
~~~
PUT 创建索引对应的mapping映射（数据类型）
~~~
http://localhost:9200/recipes/
{
    "mappings": {
        "properties": {
            "name": {
                "type": "text"
            },
            "rating": {
                "type": "float"
            },
            "type": {
                "type": "keyword"
            }
        }
    }
}
~~~



###PUT 新增数据
~~~
http://localhost:9200/recipes/type/

{
    "name": "奶油鲍鱼汤",
    "rating": 2,
    "type": "西菜"
}
~~~




###GET查看某索引下的所有数据
~~~
http://localhost:9200/recipes/_search
{
  
}
~~~


###如何删除某个索引下的所有数据？
POST  删除所有数据：（注意请求方式是Post，只删除数据，不删除表结构）

~~~
http://localhost:9200/img/_delete_by_query?pretty

{
    "query": {
    "match_all":{}
     }
}
~~~


###DEL 删除指定索引

~~~
http://localhost:9200/test
~~~


###PUT 修改数据
~~~
 http://IP:9200/shop/good/1
{
    "id":"1",
    "good_name":"【12期免息 再减600元】Apple/苹果 iPhone 11全网通4G 超广角拍照手机苏宁易购官方store 苹果11"
}
~~~



###POST 分词
~~~
http://localhost:9200/img/_analyze
{
    "analyzer":"ik_max_word",
    "text":"华为手机"
}
~~~







###GET 搜索数据
1、按某个字段查询
2、指定size返回数量  "size": 3 相当于limit 3
~~~
http://localhost:9200/recipes/type/_search
{
    "query": {
        "match": {
            "name": "鱼"
        }
    },
    "size": 3
}
~~~

2、GET 得到总数据条数Count，后面加_count就行（只查总条数）
~~~
http://localhost:9200/recipes/_count
{
    "query": {
        "match": {
            "name": "鱼"
        }
    }
}

return
{
    "count": 9,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    }
}
~~~

3、GET 查询某个索引下指定字段存在的数据集合

首先，我们要明确哪些情况认为是字段值不存在的，具体如下：

{ "tag" : null } 虽然有 tag 字段，但是值为空。
{ "tag" : [] } 虽然有 tag 字段，但是值为空数组。
{ "tag" : [null] } 虽然有 tag 字段，但是数组值为空。
{ "content" : "knowledgedict" } 没有 tag 字段。
字段值为空字符串的认为是字段值存在的。


~~~
http://localhost:9200/recipes/_search
{
  "query": {
    "exists": {
      "field": "name"
    }
  }
}
~~~


4、获取最新一条数据的方式 类似 **order by id desc limit 1**
如何获取最新一条数据，根据时间字段排序？
需要指定索引有创建时间的字段，假设创建文档的时间字段为 ***create_date***，可以如下：
```
GET {index}/_search
{
   "size": 1,
   "sort": { "create_date": "desc"},
   "query": {
      "match_all": {}
   }
}
```

此外，如果 es 的记录是通过 logstash 组建写入的，它会默认创建时间字段 ***@timestamp***，可以使用该字段。

5、只返回指定字段值 类似 **select a,b,c**

就是使用 _source 过滤器，它和 query、size、explain、from 等同级（层），_source 过滤器中在 includes 字符串数组中指定要返回的字段列表，具体如下示例：
~~~
{
  "_source" : {
    "includes" : [ "id", "title", "summary", "content", .....],
    "excludes" : [ ]
  },
  "from" : 0,
  "size" : 200,
  "explain": true, 
  "query" : ...,
  "highlight" : ...
}
~~~

6、查询指定索引的所有文档id

elasticsearch（es）获取指定索引（index）的所有文档的 id 的方法，这里的 id 指的是 es 文档内部定义的 _id。


我们可以看出 query 相关语句中指定了 stored_fields 参数，该参数本质是 lucene 里的概念，其主要用于行存储文档需要保存的字段内容，每个文档的所有 stored_fields 保存在一起，在查询请求需要返回字段原始值的时候使用。

下面返回的"_id": "LYFQkn8BwHe51sVVuu5I" 就是了

~~~
http://localhost:9200/recipes/_search
{
    "query": {
        "match_all": {}
    },
    "stored_fields": []
}

return
{
    "took": 1,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 9,
            "relation": "eq"
        },
        "max_score": 1.0,
        "hits": [
            {
                "_index": "recipes",
                "_type": "type",
                "_id": "LYFQkn8BwHe51sVVuu5I",
                "_score": 1.0
            },
            {
                "_index": "recipes",
                "_type": "type",
                "_id": "L4FQkn8BwHe51sVV4O6J",
                "_score": 1.0
            }
    }
}
~~~
