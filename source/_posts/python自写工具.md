---
title: python自写工具.md
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
title: python自写工具.md
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
1、对象是不是有某个属性

hasattr(error_box,'text')


1、is_number
~~~
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    import unicodedata
    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    if len(s) < 2:
        return False

    try:
        d = 0
        if s.startswith('－'):
            s = s[1:]
        for c in s:
            if c == '－':  # 全角减号
                return False

            if c == '．':  # 全角点号
                if d > 0:
                    return False
                else:
                    d = 1
                    continue
            unicodedata.numeric(c)
        return True
    except (TypeError, ValueError):
        pass

    return False

~~~

2、vali

def vali(list, i):
    if list:
        if i or i == 0:
            size = len(list)
            if size == 0:
                return False
            elif size - 1 >= i:
                return True

    return False
