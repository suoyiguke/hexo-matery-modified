---
title: mysql-索引原理之B+树.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-索引原理之B+树.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---


###B+树


balance tree，平衡的树。不会出现那种一边特别多层的情况。让数据都放在树的同一层。

B+树是为磁盘或其他 直接存取辅助设备设计的一种多叉平衡查找树。在B+树中,所有记录节点都是按键值的大 小顺序存放在同一层的叶子节点上,由各叶子节点指针进行连接。

平衡查找树、所有记录节点按键值大小顺序放在同一层的叶子节点上，由各叶子节点指针进行连接


###核心问题
索引效率的关键就是： 减少IO次数。 InnoDB 中 B+ 树高度一般为 1-3 层，它就能满足千万级的数据存储。
在查找数据时一次页的查找代表一次 IO，所以通过主键索引查询通常只需要 1-3 次 IO 操作即可查找到数据。


###B+树和B树的区别
B+树是B树的一个变体，B+树与B树最大的区别在于：

1、 叶子结点包含全部关键字以及指向相应记录的指针，而且叶结点中的关键字按大小顺序排列，相邻叶结点用指针连接。
2、非叶结点仅存储其子树的最大（或最小）关键字，可以看成是索引。

一棵3阶的B+树示例：（好好体会和B树的区别，两者的关键字是一样的）

![image](https://upload-images.jianshu.io/upload_images/13965490-e926e2c71ab7dbfc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###问：为什么说B+树比B树更适合实际应用中操作系统的文件索引和数据库索引？


1、B+树表示的索引范围会更大
 B+树更适合外部存储。由于内结点不存放真正的数据（只是存放其子树的最大或最小的关键字，作为索引），一个结点可以存储更多的关键字，每个结点能索引的范围更大更精确，也意味着B+树单次磁盘IO的信息量大于B树，I/O的次数相对减少。

2、 加强了区间访问性
MySQL是一种关系型数据库，**区间访问**是常见的一种情况，B+树叶结点增加的链指针，加强了区间访问性，可使用在区间查询的场景；而使用B树则无法进行区间查找。


### 页 Page Directory 和 页分裂 split

B+树索引并不能找到一个给定键值的具体行。 `B+树索引能找到的只是被查找数据行所在的页  Page Directory`。然后数据库通过把页读入到内存,再在 内存中进行查找,最后得到要查找的数据

>数据行所在页 Page Directory==>读取到内存===>从内存中查找得到需要的数据（从页中查找得到具体的数据使用是二分法查找）


每页 Page Directory中的槽是按照主键的大小顺序存放的,对于某一 条具体记录的查询是通过对 Page Directory进行二分查找得到的。

页的大小是固定的，可以通过 参数设置，mysql5.7默认大小16384，16K 。不同的硬件设备上设置页大小对性能都有影响，若要达到最佳请自己进行mysql基准测试。依次测试 4K 8K 16K 32K  
~~~
SHOW VARIABLES LIKE '%innodb_page_size%'
~~~

当页中没有更多空间容纳数据时会进行`页分裂`   也称之为`拆分页`（split）。B+树结构主要用于磁盘,页的拆分意 味着磁盘的操作,所以应该在可能的情况下荩量减少页的拆分操作

###页分裂的具体形式


###  为什么使用 B+ 树而不是B 树，B +树有什么优势？


因为 B 树不管叶子节点还是非叶子节点，都会保存数据，这样导致在非叶子节点中能保存的指针数量变少（有些资料也称为扇出 fan out），指针少的情况下要保存大量数据，只能增加树的高度，导致 IO 操作变多，查询性能变低。



###innodb中如何确认主键索引的树高度

~~~
SELECT
	b.NAME,
	a.NAME,
	index_id,
	type,
	a.space,
	a.PAGE_NO 
FROM
	information_schema.INNODB_SYS_INDEXES a,
	information_schema.INNODB_SYS_TABLES b 
WHERE
	a.table_id = b.table_id 
	AND a.space <> 0;
~~~
