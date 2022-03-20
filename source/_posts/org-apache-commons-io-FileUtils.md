---
title: org-apache-commons-io-FileUtils.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: org-apache-commons-io-FileUtils.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
~~~
 File file = new File(System.getProperty("user.dir").concat("/config/organizationId"));
        if (!file.exists()) {
            FileUtils.write(file,"你哈珀");
        }

        String s = FileUtils.readFileToString(file);
        System.out.println(s);
~~~
