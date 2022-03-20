---
title: EXPLAIN-format=json-查看查询花销.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: EXPLAIN-format=json-查看查询花销.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
https://blog.csdn.net/weixin_38004638/article/details/106427205


###字段解释
###EXPLAIN.query_block.query_cost 
查询总成本
EXPLAIN: {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "26.21" 
},

####used_key_parts
join和where中用到的索引子部分
####"using_index": true
 是否索引覆盖

####used_columns
[
            "id",
            "key1",
            "key2",
            "key3",
            "key_part1",
            "key_part2",
            "key_part3",
            "common_field"]

执行查询中涉及到的列

####nested_loop   
几个表之间采用嵌套循环连接算法执行

#### "rows_examined_per_scan": 9688
查询一次s1表大致需要扫描9688条记录

#### "rows_produced_per_join": 968,    
驱动表s1的扇出是968（估算值）

####"filtered": "10.00"
满足关联条件数据占扫描行数的比例，被驱动表上看这个没啥意义
越少最后计算的花销就越少。效率也就越高
  
#### attached_condition
 "((`mgb_treasure_system`.`d`.`del_status` = 0) and (<cache>(now()) between `mgb_treasure_system`.`d`.`gift_start_time` and `mgb_treasure_system`.`d`.`gift_end_time`))"

对d表访问时针对单表查询的where条件或者on条件

#### "access_type"
"ref"    访问方法为ref，意味着使用索引等值匹配的方式访问；就是EXPLAIN 的type字段

####cost_info是怎么计算出来的？
先看s1表的"cost_info"部分：

"cost_info": {
    "read_cost": "1840.84",
    "eval_cost": "193.76",
    "prefix_cost": "2034.60",
    "data_read_per_join": "1M" 
}
1、read_cost是由下边这两部分组成的：

- IO成本
- 检测rows × (1 - filter)条记录的CPU成本

rows和filter都是我们前边介绍执行计划的输出列，在JSON格式的执行计划中，rows相当于rows_examined_per_scan，filtered名称不变。

>2、eval_cost是这样计算的：检测 rows × filter条记录的成本。

>3、`重要`prefix_cost就是单独查询s1表的成本，也就是：read_cost + eval_cost，这个是重点关注的值

4、`重要`data_read_per_join表示在此次查询中需要读取的数据量

 

对于s2表的"cost_info"部分是这样的：

"cost_info": {
    "read_cost": "968.80",
    "eval_cost": "193.76",
    "prefix_cost": "3197.16",
    "data_read_per_join": "1M"
}
由于s2表是被驱动表，所以可能被读取多次，这里的read_cost和eval_cost是访问多次s2表后累加起来的值，大家主要关注里边儿的prefix_cost的值代表的是整个连接查询预计的成本，也就是单次查询s1表和多次查询s2表后的成本的和，也就是：

968.80 + 193.76 + 2034.60 = 3197.16


###优化例子
第一种花费  "prefix_cost": "12.20",
第二种花费 "prefix_cost":"2.40"。第二种也是用到了4个索引子部分。所以第二种更优秀
~~~
            "used_key_parts": [
              "id",
              "del_status"
            ],
            "key_length": "10",
            "ref": [
              "mgb_treasure_system.c.gift_rule_id",
              "const"
            ],
            "rows_examined_per_scan": 1,
            "rows_produced_per_join": 1,
            "filtered": "14.29",
            "cost_info": {
              "read_cost": "8.00",
              "eval_cost": "0.23",
              "prefix_cost": "12.20",
              "data_read_per_join": "1K"
            },
            "used_columns": [
              "id",
              "gift_start_time",
              "gift_end_time",
              "del_status"
            ],
~~~

~~~
  "used_key_parts":[
                            "id",
                            "del_status",
                            "gift_start_time",
                            "gift_end_time"
                        ],
                        "key_length":"22",
                        "rows_examined_per_scan":7,
                        "rows_produced_per_join":0,
                        "filtered":"14.29",
                        "using_index":true,
                        "cost_info":{
                            "read_cost":"2.20",
                            "eval_cost":"0.20",
                            "prefix_cost":"2.40",
                            "data_read_per_join":"1K"
                        },							
~~~

###查询总消耗
join 查询的总成本计算公式简化：
连接查询总成本 = 访问驱动表的成本 + 驱动表扇出数 * 单次访问被驱动表的成本。explain 执行计划详解 1 中有解释 filtered 在关联查询中的重要性。

在上面示例中：访问驱动表的成本 = 26.21，驱动表扇出数 = 18*33.33% = 6，单次访问驱动表的成本 = 1.0+0.2 总成本=26.21+6(1.0+0.2)=33.41


###比较
####字段关联，字符集不同
一个是utf8一个是utf8mb4，虽不会索引失效。但是却读取数据 "data_read_per_join": "2K"、ref=func

~~~
"key_length": "1023",
            "ref": [
              "func"
            ],
            "rows_examined_per_scan": 1,
            "rows_produced_per_join": 1,
            "filtered": "100.00",
            "using_index": true,
            "cost_info": {
              "read_cost": "1.00",
              "eval_cost": "0.20",
              "prefix_cost": "1.20",
              "data_read_per_join": "2K"
            },
            "used_columns": [
              "cat_name",
              "cat_no"
            ],
            "attached_condition": "(`my`.`product_category`.`cat_no` = convert(`my`.`a`.`cat_root_no` using utf8mb4))"
          }

~~~

~~~
"key_length": "768",
"ref": [
"my.a.cat_root_no"
],
"rows_examined_per_scan": 1,
"rows_produced_per_join": 1,
"filtered": "100.00",
"using_index": true,
"cost_info": {
"read_cost": "1.00",
"eval_cost": "0.20",
"prefix_cost": "1.20",
"data_read_per_join": "1K"
},
"used_columns": [
"cat_name",
"cat_no"
],
"attached_condition": "(`my`.`product_category`.`cat_no` = `my`.`a`.`cat_root_no`)"
}

~~~
