---
title: OLAP-和-OLTP.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: dba
categories: dba
---
---
title: OLAP-和-OLTP.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: dba
categories: dba
---

数据处理大致可以分成两大类：联机事务处理OLTP（on-line transaction processing）、联机分析处理OLAP（On-Line Analytical Processing）。

1、OLTP是传统的关系型数据库的主要应用，主要是基本的、日常的事务处理，例如银行交易。

OLTP 系统强调数据库内存效率，强调内存各种指标的命令率，强调绑定变量，强调并发操作；

2、OLAP是数据仓库系统的主要应用，支持复杂的分析操作，侧重决策支持，并且提供直观易懂的查询结果。 


OLAP 系统则强调数据分析，强调SQL执行市场，强调磁盘I/O，强调分区等。中小型OLAP应用中MyISAM使用的非常普遍，不要用MyISAM也只能说是在OLTP应用中尽量不要使用


###ETL操作
ETL(Extract-Transform-Load的缩写，即数据抽取、转换、装载的过程)作为DW的核心和灵魂，能够按照统一的规则集成并提高数据的价值，是负责完成数据从数据源向目标数据仓库转化的过程，是实施数据仓库的重要步骤。如果说数据仓库的模型设计是一座大厦的设计蓝图，数据是砖瓦的话，那么ETL就是建设大厦的过程。在整个项目中最难部分是用户需求分析和模型设计，而ETL规则设计和实施则是工作量最大的，约占整个项目的60%～80%，这是国内外从众多实践中得到的普遍共识。

ETL是数据抽取（Extract）、清洗（Cleaning）、转换（Transform）、装载（Load）的过程。是构建数据仓库的重要一环，用户从数据源抽取出所需的数据，经过数据清洗,最终按照预先定义好的数据仓库模型，将数据加载到数据仓库中去。


现在来说说ETL技术用到的工具，常用的有Informatica、Datastage、Beeload、Kettle等。目前只用过kettle，所以这里只对kettle做描述。

kettle是一款国外开源的ETL工具，纯java编写，可以在Window、Linux、Unix上运行，kettle 3版本需要安装 3以上都是绿色版无需安装。

> etl 操作主要是事务操作，使用innodb
