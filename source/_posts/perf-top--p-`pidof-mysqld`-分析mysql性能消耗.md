---
title: perf-top--p-`pidof-mysqld`-分析mysql性能消耗.md
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
title: perf-top--p-`pidof-mysqld`-分析mysql性能消耗.md
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
perf top主要用于实时分析各个函数在某个性能事件上的热度，能够快速的定位热点函数，包括应用程序函数、 
模块函数与内核函数，甚至能够定位到热点指令。默认的性能事件为cpu cycles。
~~~
[root@localhost neptuneTest]# perf top -p `pidof mysqld`                                                                                             
Samples: 221  of event 'cycles', Event count (approx.): 10810377, UID: mysql
 10.34%  mysqld            [.] my_strnncollsp_utf8                                                                                            
  5.70%  [kernel]          [k] _spin_lock_irqsave                                                                                             
  5.66%  libc-2.12.so      [.] __memset_sse2                                                                                                  
  5.55%  [kernel]          [k] remove_wait_queue                                                                                              
  5.16%  libc-2.12.so      [.] __GI___strcmp_ssse3                                                                                            
  4.36%  [kernel]          [k] __audit_syscall_exit                                                                                           
  3.39%  [kernel]          [k] lookup_ioctx                                                                                                   
  3.28%  [kernel]          [k] find_next_bit                                                                                                  
  3.22%  mysqld            [.] lex_one_token(YYSTYPE*, THD*)                                                                                  
  2.69%  mysqld            [.] Item::val_bool()                                                                                               
  2.60%  [kernel]          [k] __do_softirq                                                                                                   
  2.53%  mysqld            [.] Protocol::send_result_set_row(List<Item>*)                                                                     
  2.52%  [kernel]          [k] local_bh_enable_ip                                                                                             
  2.51%  mysqld            [.] my_strnncoll_binary                                                                                            
  2.51%  libc-2.12.so      [.] memcpy                                                                                                         
~~~


第一列：符号引发的性能事件的比例，默认指占用的cpu周期比例。 
第二列：符号所在的DSO(Dynamic Shared Object)，可以是应用程序、内核、动态链接库、模块。 
第三列：DSO的类型。[.]表示此符号属于用户态的ELF文件，包括可执行文件与动态链接库)。[k]表述此符号属于内核或模块。 
第四列：符号名。有些符号不能解析为函数名，只能用地址表示。

常用交互命令: 
h：显示帮助 
UP/DOWN/PGUP/PGDN/SPACE：上下和翻页。 
a：annotate current symbol，注解当前符号。能够给出汇编语言的注解，给出各条指令的采样率。 
d：过滤掉所有不属于此DSO的符号。非常方便查看同一类别的符号。 
P：将当前信息保存到perf.hist.N中。

常用命令行参数: 
-e ：指明要分析的性能事件。 
-p ：Profile events on existing Process ID (comma sperated list). 仅分析目标进程及其创建的线程。 
-k ：Path to vmlinux. Required for annotation functionality. 带符号表的内核映像所在的路径。 
-K：不显示属于内核或模块的符号。 
-U：不显示属于用户态程序的符号。 
-d ：界面的刷新周期，默认为2s，因为perf top默认每2s从mmap的内存区域读取一次性能数据。 
-G：得到函数的调用关系图。 
perf top -G [fractal]，路径概率为相对值，加起来为100%，调用顺序为从下往上。 
perf top -G graph，路径概率为绝对值，加起来为该函数的热度。
