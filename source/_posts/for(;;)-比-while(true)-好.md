---
title: for(;;)-比-while(true)-好.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: for(;;)-比-while(true)-好.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---

为啥:如下（底层完全不同）

“死循环”有两种写法：for(;;)和while(true)，
两者有啥区别，为啥源码中多数是for( ; ; )这种形式的，
~~~
  编译前              编译后 
while (1)；         mov eax,1  
                    test eax,eax 
                    je foo+23h
                    jmp foo+18h
    编译前              编译后 
for (；；)；          jmp foo+23h 　　
~~~
对比之下，for (；；)指令少，不占用寄存器，而且没有判断跳转，比while (1)好。

也就是说两者在在宏观上完全一样的逻辑，但是底层完全不一样，for相对于来说更加简洁明了。


for循环和Iterator结合使用：

~~~
    void removeEQ(Object o) {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
            for (Iterator<E> it = q.iterator(); it.hasNext(); ) {
                if (o == it.next()) {
                    it.remove();
                    break;
                }
            }
        } finally {
            lock.unlock();
        }
    }

~~~
