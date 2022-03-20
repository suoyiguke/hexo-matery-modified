---
title: Use-of-Index-Extensions--索引扩展的使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: Use-of-Index-Extensions--索引扩展的使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
https://dev.mysql.com/doc/refman/8.0/en/index-extensions.html

[`InnoDB`](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html "第 15 章 InnoDB 存储引擎")通过向其附加主键列来自动扩展每个二级索引。考虑这个表定义：

```
CREATE TABLE t1 (
  i1 INT NOT NULL DEFAULT 0,
  i2 INT NOT NULL DEFAULT 0,
  d DATE DEFAULT NULL,
  PRIMARY KEY (i1, i2),
  INDEX k_d (d)
) ENGINE = InnoDB;
```

该表定义了列上的主键`(i1, i2)`。它还`k_d`在列上定义了一个二级索引 `(d)`，但在内部`InnoDB`扩展了该索引并将其视为列`(d, i1, i2)`。

在确定如何以及是否使用该索引时，优化器会考虑扩展二级索引的主键列。这可以产生更高效的查询执行计划和更好的性能。

优化器可以将扩展二级索引用于 `ref`、`range`和 [`index_merge`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_index-merge)索引访问、松散索引扫描访问、连接和排序优化以及 [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)/[`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max) 优化。

以下示例显示了执行计划如何受优化器是否使用扩展二级索引的影响。假设`t1`用这些行填充：

```
INSERT INTO t1 VALUES
(1, 1, '1998-01-01'), (1, 2, '1999-01-01'),
(1, 3, '2000-01-01'), (1, 4, '2001-01-01'),
(1, 5, '2002-01-01'), (2, 1, '1998-01-01'),
(2, 2, '1999-01-01'), (2, 3, '2000-01-01'),
(2, 4, '2001-01-01'), (2, 5, '2002-01-01'),
(3, 1, '1998-01-01'), (3, 2, '1999-01-01'),
(3, 3, '2000-01-01'), (3, 4, '2001-01-01'),
(3, 5, '2002-01-01'), (4, 1, '1998-01-01'),
(4, 2, '1999-01-01'), (4, 3, '2000-01-01'),
(4, 4, '2001-01-01'), (4, 5, '2002-01-01'),
(5, 1, '1998-01-01'), (5, 2, '1999-01-01'),
(5, 3, '2000-01-01'), (5, 4, '2001-01-01'),
(5, 5, '2002-01-01');
```

现在考虑这个查询：

```
EXPLAIN SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01'
```

执行计划取决于是否使用扩展索引。

当优化器不考虑索引扩展时，它只将索引`k_d`视为`(d)`. [`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html "13.8.2 EXPLAIN 语句")对于查询产生此结果：

```
mysql> EXPLAIN SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01'\G
*************************** 1\. row ***************************
           id: 1
  select_type: SIMPLE
        table: t1
         type: ref
possible_keys: PRIMARY,k_d
          key: k_d
      key_len: 4
          ref: const
         rows: 5
        Extra: Using where; Using index
```

当优化需要索引扩展到帐户，它把`k_d`作为`(d, i1, i2)`。在这种情况下，它可以使用最左边的索引前缀`(d, i1)`来生成更好的执行计划：

```
mysql> EXPLAIN SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01'\G
*************************** 1\. row ***************************
           id: 1
  select_type: SIMPLE
        table: t1
         type: ref
possible_keys: PRIMARY,k_d
          key: k_d
      key_len: 8
          ref: const,const
         rows: 1
        Extra: Using index
```

在这两种情况下，`key`表示优化器使用二级索引，`k_d`但 [`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html "13.8.2 EXPLAIN 语句")输出显示了使用扩展索引的这些改进：

*   `key_len`从 4 个字节变为 8 个字节，表明键查找使用列`d` 和`i1`，而不仅仅是`d`.

*   该`ref`值从改变 `const`到`const,const` ，因为键查找使用两个关键部分，没有之一。

*   的`rows`计数降低从5到1，表明`InnoDB`应该需要检查更少的行，以产生结果。

*   该`Extra`值从变化 `Using where; Using index`到 `Using index`。这意味着可以仅使用索引读取行，而无需查询数据行中的列。

使用扩展索引的优化器行为的差异也可以通过以下方式看到[`SHOW STATUS`](https://dev.mysql.com/doc/refman/8.0/en/show-status.html "13.7.7.37 显示状态语句")：

```
FLUSH TABLE t1;
FLUSH STATUS;
SELECT COUNT(*) FROM t1 WHERE i1 = 3 AND d = '2000-01-01';
SHOW STATUS LIKE 'handler_read%'
```

前面的语句包括[`FLUSH TABLES`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-tables)和[`FLUSH STATUS`](https://dev.mysql.com/doc/refman/8.0/en/flush.html#flush-status) 刷新表缓存并清除状态计数器。

没有索引扩展，[`SHOW STATUS`](https://dev.mysql.com/doc/refman/8.0/en/show-status.html "13.7.7.37 显示状态语句")产生这个结果：

```
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| Handler_read_first    | 0     |
| Handler_read_key      | 1     |
| Handler_read_last     | 0     |
| Handler_read_next     | 5     |
| Handler_read_prev     | 0     |
| Handler_read_rnd      | 0     |
| Handler_read_rnd_next | 0     |
+-----------------------+-------+
```

使用索引扩展，[`SHOW STATUS`](https://dev.mysql.com/doc/refman/8.0/en/show-status.html "13.7.7.37 显示状态语句")产生这个结果。该 [`Handler_read_next`](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Handler_read_next)值从 5 减少到 1，表明索引的使用效率更高：

```
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| Handler_read_first    | 0     |
| Handler_read_key      | 1     |
| Handler_read_last     | 0     |
| Handler_read_next     | 1     |
| Handler_read_prev     | 0     |
| Handler_read_rnd      | 0     |
| Handler_read_rnd_next | 0     |
+-----------------------+-------+
```

系统变量 的[`use_index_extensions`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_use-index-extensions)标志[`optimizer_switch`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_optimizer_switch)允许控制优化器在确定如何使用`InnoDB`表的二级索引时是否考虑主键列 。默认情况下，[`use_index_extensions`](https://dev.mysql.com/doc/refman/8.0/en/switchable-optimizations.html#optflag_use-index-extensions) 已启用。要检查禁用索引扩展是否可以提高性能，请使用以下语句：

```
SET optimizer_switch = 'use_index_extensions=off';
```

优化器对索引扩展的使用受到索引中关键部分数量 (16) 和最大密钥长度 (3072 字节) 的通常限制。
