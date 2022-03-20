---
title: IK分词器ik_smart和ik_max_word区别.md
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
title: IK分词器ik_smart和ik_max_word区别.md
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
###ik_smart和ik_max_word区别


1、ik_max_word

会将文本做最细粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为“中华人民共和国、中华人民、中华、华人、人民共和国、人民、共和国、大会堂、大会、会堂等词语。
~~~
{
    "tokens": [
        {
            "token": "中华人民共和国",
            "start_offset": 0,
            "end_offset": 7,
            "type": "CN_WORD",
            "position": 0
        },
        {
            "token": "中华人民",
            "start_offset": 0,
            "end_offset": 4,
            "type": "CN_WORD",
            "position": 1
        },
        {
            "token": "中华",
            "start_offset": 0,
            "end_offset": 2,
            "type": "CN_WORD",
            "position": 2
        },
        {
            "token": "华人",
            "start_offset": 1,
            "end_offset": 3,
            "type": "CN_WORD",
            "position": 3
        },
        {
            "token": "人民共和国",
            "start_offset": 2,
            "end_offset": 7,
            "type": "CN_WORD",
            "position": 4
        },
        {
            "token": "人民",
            "start_offset": 2,
            "end_offset": 4,
            "type": "CN_WORD",
            "position": 5
        },
        {
            "token": "共和国",
            "start_offset": 4,
            "end_offset": 7,
            "type": "CN_WORD",
            "position": 6
        },
        {
            "token": "共和",
            "start_offset": 4,
            "end_offset": 6,
            "type": "CN_WORD",
            "position": 7
        },
        {
            "token": "国人",
            "start_offset": 6,
            "end_offset": 8,
            "type": "CN_WORD",
            "position": 8
        },
        {
            "token": "人民大会堂",
            "start_offset": 7,
            "end_offset": 12,
            "type": "CN_WORD",
            "position": 9
        },
        {
            "token": "人民大会",
            "start_offset": 7,
            "end_offset": 11,
            "type": "CN_WORD",
            "position": 10
        },
        {
            "token": "人民",
            "start_offset": 7,
            "end_offset": 9,
            "type": "CN_WORD",
            "position": 11
        },
        {
            "token": "大会堂",
            "start_offset": 9,
            "end_offset": 12,
            "type": "CN_WORD",
            "position": 12
        },
        {
            "token": "大会",
            "start_offset": 9,
            "end_offset": 11,
            "type": "CN_WORD",
            "position": 13
        },
        {
            "token": "会堂",
            "start_offset": 10,
            "end_offset": 12,
            "type": "CN_WORD",
            "position": 14
        }
    ]
}
~~~

2、ik_smart
会做最粗粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为中华人民共和国、人民大会堂。
 ~~~
http://localhost:9200/img/_analyze
{
    "analyzer":"ik_smart",
    "text":"中华人民共和国人民大会堂"
}
{
    "tokens": [
        {
            "token": "中华人民共和国",
            "start_offset": 0,
            "end_offset": 7,
            "type": "CN_WORD",
            "position": 0
        },
        {
            "token": "人民大会堂",
            "start_offset": 7,
            "end_offset": 12,
            "type": "CN_WORD",
            "position": 1
        }
    ]
}
~~~

###最佳实践
两种分词器使用的最佳实践是：索引时用ik_max_word，在搜索时用ik_smart
 

搜索时，输入“华为手机”，此时是想搜索出“华为手机”的商品，而不是华为其它的商品


此时使用ik_smart和ik_max_word都会将华为手机拆分为华为和手机两个词，那些只包括“华为”这个词的信息也被搜索出来了，我的目标是搜索只包含华为手机这个词的信息，这没有满足我的目标。

怎么解决呢？
我们可以将华为手机添加到**自定义词库**，

这样，因为华为手机是一个词，所以ik_smart不再细粒度分了

 


如果我想将包含华为 这个词的信息也搜索出来怎么办呢？
那就输入 “华为 华为手机”（注意华为后边有个空格），那就会将包含华为、华为手机的信息都搜索出来。

 

备注：

@Field(type=FieldType.Text, analyzer="ik_max_word")     表示该字段是一个文本，并作最大程度拆分，默认建立索引

@Field(type=FieldType.Text,index=false)             表示该字段是一个文本，不建立索引

@Field(type=FieldType.Date)                                表示该字段是一个文本，日期类型，默认不建立索引

@Field(type=FieldType.Long)                               表示该字段是一个长整型，默认建立索引

@Field(type=FieldType.Keyword)                         表示该字段内容是一个文本并作为一个整体不可分，默认建立索引

@Field(type=FieldType.Float)                               表示该字段内容是一个浮点类型并作为一个整体不可分，默认建立索引

 

date 、float、long都是不能够被拆分的
