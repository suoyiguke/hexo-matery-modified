---
title: 好用的ToolUtils.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 工具类
categories: 工具类
---
---
title: 好用的ToolUtils.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 工具类
categories: 工具类
---
ToolUtils.isEmpty 各种类型的判断空

能够使用在大多种情况，有种情况要注意下，下面会报空指针
~~~
     String zz = null;
        final boolean oneEmpty = isOneEmpty(zz, zz.hashCode() );
        System.out.println(oneEmpty);
~~~

这个时候只能使用 短路或||
~~~
  String zz = null;
        if(ToolUtil.isEmpty(zz)||ToolUtil.isEmpty(zz.hashCode())){
            
        }
~~~


工具类：

~~~
package com.gbm.cloud.common.util;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * 空参数校验工具类
 */
public class ToolUtils{


    /**
     * 对象是否不为空(新增)
     */
    public static boolean isNotEmpty(Object o) {
        return !ValidateUtil.isEmpty(o);
    }

    /**
     * 全都不为空(新增)
     */
    public static boolean isNotEmptyAll(Object... os) {
        return !ValidateUtil.isOneEmpty(os);
    }
    /**
     * 对象是否为空
     */
    public static boolean isEmpty(Object o) {
        if (o == null) {
            return true;
        }
        if (o instanceof String) {
            if (o.toString().trim().equals("")) {
                return true;
            }
        } else if (o instanceof List) {
            if (((List) o).size() == 0) {
                return true;
            }
        } else if (o instanceof Map) {
            if (((Map) o).size() == 0) {
                return true;
            }
        } else if (o instanceof Set) {
            if (((Set) o).size() == 0) {
                return true;
            }
        } else if (o instanceof Object[]) {
            if (((Object[]) o).length == 0) {
                return true;
            }
        } else if (o instanceof int[]) {
            if (((int[]) o).length == 0) {
                return true;
            }
        } else if (o instanceof long[]) {
            if (((long[]) o).length == 0) {
                return true;
            }
        }
        return false;
    }

    /**
     * 对象组中是否存在空对象
     */
    public static boolean isOneEmpty(Object... os) {
        for (Object o : os) {
            if (ValidateUtil.isEmpty(o)) {
                return true;
            }
        }
        return false;
    }

    /**
     * 对象组中是否全是空对象
     */
    public static boolean isAllEmpty(Object... os) {
        for (Object o : os) {
            if (!ValidateUtil.isEmpty(o)) {
                return false;
            }
        }
        return true;
    }

   public static boolean equalsAny(CharSequence string, CharSequence... searchStrings){
        if (ArrayUtils.isNotEmpty(searchStrings)) {
            for (CharSequence next : searchStrings) {
                if (Objects.equals(string, next)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * 拷贝属性，为null的不拷贝
     */
    public static void copyProperties(Object source, Object target) {
        BeanUtil.copyProperties(source, target, CopyOptions.create().setIgnoreNullValue(true));
    }


}

~~~




