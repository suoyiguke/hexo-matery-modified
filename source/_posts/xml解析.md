---
title: xml解析.md
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
title: xml解析.md
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
xml转json

~~~
    <dependency>
      <groupId>org.json</groupId>
      <artifactId>json</artifactId>
      <version>20201115</version>
    </dependency>
~~~
~~~
    public static void main(String[] args) {
        String xml= "<ESBEntry><AccessControl><SysFlag>1</SysFlag><UserName>CA</UserName><Password>123456</Password><Fid>BS10003</Fid><OrderNo>BS10003S16001</OrderNo></AccessControl><MessageHeader><Fid>BS10003</Fid><OrderNo>BS10003S16001</OrderNo><SourceSysCode>S16</SourceSysCode><TargetSysCode>S00</TargetSysCode><HospCode>GH01</HospCode><MsgDate>2021-03-25 15:44:55</MsgDate></MessageHeader><RequestOption><triggerData>0</triggerData><dataAmount>500</dataAmount></RequestOption><MsgInfo flag=\"1\" ><Msg/><distinct value=\"0\"/><query item=\"INHOSP_INDEX_NO\" compy=\"=\" value=\"'351372'\" splice=\"AND\"/></MsgInfo><GroupInfo flag=\"0\"><AS ID=\"\" linkField=\"\"/></GroupInfo></ESBEntry>";
        String s = XML.toJSONObject(xml).toString();
        System.out.println(s);

    }
~~~
