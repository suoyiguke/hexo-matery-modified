---
title: windows-tcp动态端口被占用过多，导致没有空闲的端口完成http请求。（发现很多TIME_WAIT状态的TCP连接）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: TCP
categories: TCP
---
---
title: windows-tcp动态端口被占用过多，导致没有空闲的端口完成http请求。（发现很多TIME_WAIT状态的TCP连接）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: TCP
categories: TCP
---
###出现问题的原因和背景


使用windows做服务器，默认TIME_WAIT的TCP连接回收时间是4分钟，TCP默认动态端口范围为开始端口49152，结束端口65535，可用端口16384个。一旦tps过大那么可能导致端口不够用。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9db69bd6d438134.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###先了解下三种端口范围

按端口号可分为3大类：

（1）公认端口（Well Known Ports）：从0到1023，它们紧密绑定（binding）于一些服务。通常这些端口的通讯明确表明了某种服务的协议。例如：80端口实际上总是HTTP通讯。

（2）注册端口（Registered Ports）：从1024到49151。它们松散地绑定于一些服务。也就是说有许多服务绑定于这些端口，这些端口同样用于许多其它目的。例如：许多系统处理动态端口从1024左右开始。

（3）动态和/或私有端口（Dynamic and/or Private Ports）：从49152到65535。理论上，不应为服务分配这些端口。实际上，机器通常从1024起分配动态端口。但也有例外：SUN的RPC端口从32768开始。




###解决方式

1、设置超时时间为30秒，30秒之后回收回收端口
>确定 TCP/IP 在释放已关闭的连接并再次使用其资源前必须经过的时间。关闭与释放之间的这段时间称为 TIME_WAIT 状态或者两倍最大段生存期（2MSL）状态。此时间期间，重新打开到客户机和服务器的连接的成本少于建立新连接。通过减少此条目的值，TCP/IP 可以更快地释放关闭的连接，并为新连接提供更多资源。如果运行中的应用程序要求快速释放连接或创建新连接，或者由于多个连接处于 TIME_WAIT 状态而导致吞吐量较低，请调整此参数。注意在Windows系统中，这个注册表键值就直接等于TIME_WAIT到CLOSED状态的等待市场，也就是2MSL的值

在“注册表编辑器”中打
开“HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters”路径。
在“编辑”菜单中，选择“新建 > DWORD （32-位）值”，输入名称“TcpTimedWaitDelay”。
右键单击TcpTimedWaitDelay，选择“修改”。
在“编辑 DWORD（32位）值”对话框的“基数”区域中，选择十进制值为“30”，并“确定”。
关闭注册表编辑器。然后需要重启电脑配置才会生效！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cdaab5a94ce82135.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>思考：若TcpTimedWaitDelay设置过小会引发什么问题？

2、设置 tcp 动态端口范围

查看
~~~
C:\IAS\8087\V2.2.16-base-release>netsh int ipv4 show dynamicportrange tcp

Protocol tcp Dynamic Port Range
---------------------------------
Start Port      : 1025
Number of Ports : 58976

~~~

设置
~~~
netsh int ipv4 set dynamicportrange tcp startport=1025 numberofports=58976
~~~
重启操作系统。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b23f993c08992a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###查看当前系统tcp下所有tcp占用端口


 windows下查看当前所有的tcp连接
~~~
netstat -ano 
~~~

 windows下查看所有8080端口的tcp连接
~~~
netstat -ano |findstr "8080" 
 ~~~
windows下查看所有的“TIME_WAIT”状态的tcp连接
~~~
netstat -ano |findstr "TIME_WAIT"  
 ~~~

 windows下统计time_wait出现的次数（按行统计） /i 忽略大小写
~~~
netstat -ano |find /i /c "TIME_WAIT"  
~~~


###重现问题

1、设置tcp数量为300
~~~
netsh int ipv4 set dynamicportrange tcp startport=1025 numberofports=300
~~~

2、编写代码测试

~~~

 public static void main(String[] args) {

        for (int i = 0; i < 10; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    String errMsg = "";
                    String  respResult="";
                    while (true){
                        //不需要工号的
                        String url = Config.GetInstance().getCloudsignAuthorizedRemoteEndpoint()
                            + "/cloudkeyserver/api/login/qrcode/nostatus/2CKV1";

                        try {
                            respResult = HttpsClientUtils.getHttpsClientUtils().HttpsPost(
                                url,
                                JSONObject.toJSONString(new HashMap<String, Object>(3) {{
                                    put("type", Constants.STATELESSNESS_NETCA_QRCODE_TYPE);
                                    put("projectUid", Config.GetInstance().getCloudsignAuthorizedAppSecret());
                                    put("applicationId", Config.GetInstance().getCloudsignAuthorizedAppID());
                                }}));
                        } catch (Exception e) {
                            errMsg = String.format("send requests to backend of NETCA catch "
                                + "CaHelperException:%s", e.getMessage());
                            System.out.println(errMsg);
                        }
                        JSONObject jsonObject = JSON.parseObject(respResult);
                        System.out.println(jsonObject.toJSONString());
                    }
                }
            }).start();

        }


    }
~~~

报错：`org.szwj.ca.identityauthsrv.controller.cloudsign.CloudsignException: send requests to backend of NETCA catch CaHelperException:No buffer space available (maximum connections reached?): connect`
问题重现！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-995aebd29bcd041f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


