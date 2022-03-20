---
title: python检测m3u8视频文件是否可播.md
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
title: python检测m3u8视频文件是否可播.md
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
一般m3u8格式只是一个索引文件，没办法直接根据这个文件来判断。因为视频不能播但是也能下载到这个文件
~~~
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-ALLOW-CACHE:YES
#EXT-X-TARGETDURATION:9
#EXTINF:8.400000,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000000.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000001.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000002.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000003.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000004.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000005.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000006.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000007.ts
#EXTINF:8.333333,
/ADUOa15mUmEKMFswAzYEbw==_2019_07_29_zhanqi_AD4OZF5tUmUKNFs5_000008.ts
#EXTINF:8.333333
~~~

可以解析这个，拿到里面的ts文件的播放路径，然后使用py的request.urlopen函数来判断，如果状态码为200则表示可播

### python例子
~~~

from urllib import request
from urllib.parse import urlparse

import requests


#替换字符串string中指定位置p的字符为c
def sub(string,p,c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)

def readM3U8(url):
    s_url = None
    response = requests.get(url)
    response.encoding = 'utf-8'
    str = response.text
    result = urlparse(url)
    url_tou = result[0] + '://' + result[1]

    # 获取m3u8中的片段ts文件
    # 需要替换 ../
    list = str.split("\n");
    for str in list:

        if str.find(".ts") != -1:
            # 特殊格式==>回退目录
            if (str.find("../../../../..") != -1):
                s_url = str.replace("../../../../..", url_tou)
            # 普通格式，直接替换，如果ts文件的开头是/则表示根目录
            else:
                if str[0:1] == '/':
                    s_url = sub(str, 0,url_tou+"/")
                else:
                    pos = url.rfind("/")
                    s_url = url.replace(url[pos:], "/"+str)

            break

    return discernVedio(s_url)

# 返回True可播放，false不可播放
def discernVedio(url):
    try:
        with request.urlopen(url) as file:
            if file.status != 200:
                return False
            else:
                return True
    except BaseException as err:
        return False


if __name__ == '__main__':
   print(discernVedio('https://record.zhanqi.tv/960186-CD4AYwo4U2cPMgphVGRSNFE2AXVXawFnVDcKPwg/DD8=.m3u8'))




~~~
