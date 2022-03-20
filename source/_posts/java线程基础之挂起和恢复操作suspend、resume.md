---
title: java线程基础之挂起和恢复操作suspend、resume.md
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
title: java线程基础之挂起和恢复操作suspend、resume.md
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

suspend 将线程状态变为 timed_waiting
resume 则是恢复成 RUNNABLE

>使用这种方式挂起和恢复线程已经过时了，可以使用wait - notify 机制代替之


~~~
    /**
     * 暂停
     *
     * @param tableName
     * @return
     */
    @RequestMapping("/pause")
    @ResponseBody
    public String pause(@RequestParam(name = "tableName", required = true) String tableName) {
        Thread thread = threadMap.get(tableName);
        thread.suspend();
        return "任务挂起";


    }

    /**
     * 恢复
     *
     * @param tableName
     * @return
     */
    @RequestMapping("/resume")
    @ResponseBody
    public String resume(@RequestParam(name = "tableName", required = true) String tableName) {

        Thread thread = threadMap.get(tableName);
        thread.resume();
        return "任务恢复";
    }
~~~

###新jdk中替代的方案

~~~
package com.data.collection.job;

class NewThread implements Runnable {

    String name; // name of thread
    Thread t;
    boolean suspendFlag;

    NewThread(String threadname) {
        name = threadname;
        t = new Thread(this, name);
        System.out.println("New thread: " + t);
        suspendFlag = false;
        t.start(); // Start the thread
    }

    // This is the entry point for thread.
    @Override
    public void run() {
        try {
            for (int i = 15; i > 0; i--) {
                System.out.println(name + ": " + i);
                Thread.sleep(200);
                synchronized (this) {
                    while (suspendFlag) {
                        wait();
                    }
                }
            }
        } catch (InterruptedException e) {
            System.out.println(name + " interrupted.");
        }
        System.out.println(name + " exiting.");
    }

    void mysuspend() {
        suspendFlag = true;
    }

    synchronized void myresume() {
        suspendFlag = false;
        notify();
    }
}

class SuspendResume {

    public static void main(String args[]) {
        NewThread ob1 = new NewThread("One");
        NewThread ob2 = new NewThread("Two");
        try {
            Thread.sleep(1000);
            ob1.mysuspend();
            System.out.println("Suspending thread One");
            Thread.sleep(1000);
            ob1.myresume();
            System.out.println("Resuming thread One");
            ob2.mysuspend();
            System.out.println("Suspending thread Two");
            Thread.sleep(1000);
            ob2.myresume();
            System.out.println("Resuming thread Two");
        } catch (InterruptedException e) {
            System.out.println("Main thread Interrupted");
        }
        // wait for threads to finish
        try {
            System.out.println("Waiting for threads to finish.");
            ob1.t.join();
            ob2.t.join();
        } catch (InterruptedException e) {
            System.out.println("Main thread Interrupted");
        }
        System.out.println("Main thread exiting.");
    }
}
~~~

###举一反三，应用下

~~~
package com.data.collection.job;

import com.data.collection.data.DataSendMain;
import java.util.Date;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Component;


@Component
@Data
@NoArgsConstructor
public class JobClass implements Runnable {

    volatile static Boolean suspendFlag = false;


    private DataSendMain dataSendMain;
    private String tableName;
    private Date sDate;
    private Date eDate;


    public JobClass(DataSendMain dataSendMain, String tableName, Date sDate, Date eDate) {
        this.dataSendMain = dataSendMain;
        this.tableName = tableName;
        this.sDate = sDate;
        this.eDate = eDate;
    }


    /**
     * 挂起
     */
    public void mysuspend() {
        suspendFlag = true;
    }

    /**
     * 恢复
     */
    public void myresume() {

        synchronized (tableName) {
            suspendFlag = false;
            tableName.notify();
        }


    }

    @Override
    public void run() {

//       ScheduleApplication.threadMap.put(tableName,Thread.currentThread());
        ScheduleApplication.jobMap.put(tableName, this);

        /**
         * 业务逻辑
         */
        dataSendMain.commomMain(tableName, sDate, eDate);

        /**
         * 线程挂起实现
         */
        synchronized (tableName) {
            while (suspendFlag) {
                try {
                    tableName.wait();
                } catch (InterruptedException e) {
                    System.out.println(tableName + " interrupted.");
                }
            }

        }

    }
}
~~~

调用

~~~

    /**
     * 暂停
     *
     * @param tableName
     * @return
     */
    @RequestMapping("/pause")
    @ResponseBody
    public String pause(@RequestParam(name = "tableName", required = true) String tableName) {

        JobClass jobClass = jobMap.get(tableName);
        jobClass.mysuspend();

        return "任务挂起";


    }

    /**
     * 恢复
     *
     * @param tableName
     * @return
     */
    @RequestMapping("/resume")
    @ResponseBody
    public String resume(@RequestParam(name = "tableName", required = true) String tableName) {

        JobClass jobClass = jobMap.get(tableName);
        jobClass.myresume();
        return "任务恢复";
    }
~~~
