---
title: MultipartFile处理方法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: MultipartFile处理方法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
注意： 
MultipartFile.transferTo（） 需要的事相对路径

file.transferTo 方法调用时，判断如果是相对路径，则使用temp目录，为父目录

一则，位置不对，二则没有父目录存在，因此产生上述错误。

//1.使用此方法保存必须指定盘符（在系统配置时要配绝对路径）;
      // 也可以通过 File f = new File(new File(path).getAbsolutePath()+ "/" + fileName); 取得在服务器中的绝对路径 保存即可
//      file.transferTo(f);

      //2.使用此方法保存可相对路径（/var/falcon/）也可绝对路径（D:/var/falcon/）
      byte [] bytes = file.getBytes();
      OutputStream out = new FileOutputStream(f);
      out.write(bytes);
45
