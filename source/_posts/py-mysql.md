---
title: py-mysql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: py-mysql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
session发出原生sql
~~~

    session = getSession()
    session.begin(subtransactions=True)
    cursor = session.execute("SELECT yk FROM tb WHERE id = 1;")
    result = cursor.first()
    yk = result[0]
    yk = yk + 1

    execute = session.execute("UPDATE `test`.`tb` SET `yk` = :yk WHERE `id` = 1;", {"yk": yk})
    print(execute)

    session.commit()
    session.close()
~~~
