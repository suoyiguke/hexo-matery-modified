---
title: TableField注解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: @TableField注解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
Plus会遇到插入数据的时候，比如每条数据插入修改人、修改时间、创建人创建时间。可以自动填充



    @TableField(value = "create_time", fill = FieldFill.INSERT)
自定义值传入
