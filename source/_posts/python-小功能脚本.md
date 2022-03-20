---
title: python-小功能脚本.md
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
title: python-小功能脚本.md
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
######发起http请求，解析json
~~~
import json
import requests
response = requests.get('https://is-hl.snssdk.com/api/news/feed/v88/?st_time=709&sati_extra_params=%7B"last_click_item_list"%3A%5B%5D%7D&ad_ui_style=%7B"is_crowd_generalization_style"%3A0%7D&list_count=65&support_rn=0&concern_id=6286225228934679042&refer=1&count=20&max_behot_time=1569132304&last_refresh_sub_entrance_interval=1569140663&plugin_enable=3&client_extra_params=%7B"playparam"%3A"codec_type%3A0"%2C"lynx_version_json"%3A"%7B%5C"live_chat_header%5C"%3A73801%2C%5C"ugc_lynx_hotboard%5C"%3A74001%7D"%7D&gps_mode=5&loc_mode=1&tt_from=pre_load_more&lac=4527&cid=28883&iid=86986794354&device_id=69571417789&ac=wifi&channel=wandoujia2&aid=13&app_name=news_article&version_code=742&version_name=7.4.2&device_platform=android&ab_version=814658%2C1103041%2C662176%2C1160510%2C762215%2C665175%2C674050%2C643892%2C1052634%2C649427%2C801968%2C707372%2C661903%2C668775%2C1163477%2C1181110%2C1184630%2C1066377%2C1138488%2C1156308%2C1157750%2C1157634%2C1185616%2C1177115%2C668779%2C662099%2C1173123%2C1183130%2C1137770%2C1184410%2C668774%2C1172158%2C1154098%2C765197%2C1176943%2C857804%2C1152356%2C757281%2C1166283%2C679101%2C1095474%2C660830%2C1054755%2C1175193%2C759653%2C661781%2C648317&ab_group=100169&ab_feature=102749%2C94563&ssmix=a&device_type=vivo+X20A&device_brand=Android&language=zh&os_api=22&os_version=5.1.1&uuid=865166010344193&openudid=34415d7573851286&manifest_version_code=742&resolution=720*1280&dpi=240&update_version_code=74211&_rticket=1569140663372&plugin=0&tma_jssdk_version=1.34.0.4&rom_version=22&cdid=ac0c1792-3d96-4efa-b04b-74804c788606&ts=1569140665&as=ab9930be485d872fb79930&mas=0119932313997933f3a3a379b985decbd233f3a3a3d3795973d323&cp=50d58c7f2cfb7q1'.replace("\n", ""))
print(response.text)
js = json.loads(response.text)
print(js)
~~~

######post请求
~~~
    "businessOrgCode":"455767873",
    "businessSystemAppID":"o7d7q8ehm4tkrc6o",
    "relBizNo": "13725291113",
    "name": "yinkai",
    "idCardNo": "43040519970627501X",
    "phoneNo": "13725291113",
    "type": "0",
    "gender": 0,
    "identityType":2,
    "businessSystemCode":1000
})
print(response.text)
js = json.loads(response.text)
print(js)
~~~

######统计代码运行时间
~~~
import time
time_start = time.time()  # 开始计时

time.sleep(2)

time_end = time.time()  # 结束计时

time_c = time_end - time_start  # 运行所花时间
# 打印秒数
print('耗时', time_c, 's')

# 打印 时分秒
m, s = divmod(time_c, 60)
h, m = divmod(m, 60)
print ("%02d:%02d:%02d" % (h, m, s))
~~~

######日期接口测试
需要传入时间作为参数，时间可以循环变化
~~~
import datetime

from time import strftime, localtime
from datetime import timedelta, date
import calendar


import requests

# 发出接口请求http://v.17173.com/api/video/vInfo/id/33031272?t=1552988099999,可获得视频真实路径
import logger
log = logger.logger()

def get_day_of_day(date,n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date - timedelta(days=n)
    else:
        return date + timedelta(days=n)


def get_day_nday_ago(date,n):
    t = datetime.datetime.strptime(date, "%Y-%m-%d")
    return get_day_of_day(t,n)

# 示例

i=0
while True:
    url_json = 'http://localhost:8081/api/user/t/getUserNew?userId=70&date={i}'.format(i=get_day_nday_ago('2019-08-01',i).strftime("%Y-%m-%d"))  # 2020-03-19 18:18:35
    log.debug(url_json)
    response = requests.get(url_json.strip().replace("\n", ""))
    response.encoding = 'utf-8'
    log.debug(response.text)
    i=i+1
~~~

######不下载网络文件，只是查看http请求状态
如果链接指向一个文件也不怕，因为file在调用read()方法前不会下载内容。
~~~
from urllib import request

with request.urlopen("http://huya-w7.huya.com/1912/136902395/1300/048e7b14d662055e6bb1dbbbd37ef3f3.mp4") as file:
    print(file.status)
    print(file.reason)
    print(file)
~~~
######下载网络文件到本地
~~~
import wget

# 网络地址
DATA_URL = "http://v-replay-ks.cdn.huya.com/vhuya/dot/2258195946/6671491529808037654/17694299/04:31:50_04:32:57_yuanhua.m3u8"
# 本地硬盘文件
out_fname = './zz.m3u8'

wget.download(DATA_URL, out=out_fname)
~~~

######直接读取网络文件
~~~
import requests

response = requests.get("http://v-replay-ks.cdn.huya.com/vhuya/dot/2258195946/6671491529808037654/17694299/04:31:50_04:32:57_yuanhua.m3u8")
response.encoding = 'utf-8'
print(response.text)
~~~
######读取properties配置文件
~~~
class Properties(object):

    def __init__(self, fileName):
        self.fileName = fileName
        self.properties = {}

    def __getDict(self,strName,dictName,value):

        if(strName.find('.')>0):
            k = strName.split('.')[0]
            dictName.setdefault(k,{})
            return self.__getDict(strName[len(k)+1:],dictName[k],value)
        else:
            dictName[strName] = value
            return
    def getProperties(self):
        try:
            pro_file = open(self.fileName, 'r')
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#")!=-1:
                    line=line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1]= line[len(strs[0])+1:]
                    self.__getDict(strs[0].strip(),self.properties,strs[1].strip())
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return self.properties


# 测试
if __name__ == '__main__':
    properties = Properties("dblink.properties").getProperties()

    print(int(properties['port']))
~~~

######使用模拟cookie发出http请求
~~~
import requests
from requests.cookies import RequestsCookieJar

url = 'https://share.egame.qq.com/cgi-bin/pgg_async_fcgi?g_tk=1811021702&_=1554276299137&param={"0":{"module":"pgg.vod_material_warehouse_srf_svr.CPggVodMaterialWarehouseSrfSvrObj","method":"GetMaterialList","param":{"material_type":1,"begin_ts":1554134400,"end_ts":1554220799,"app_id":"1104466820","anchor_id":0,"page_size":20,"page_num":1}}}&app_info={"platform":4,"terminal_type":2,"egame_id":"egame_open_mng","version_code":"9.9.9.9","version_name":"9.9.9.9"}'

cookie_jar = RequestsCookieJar()
cookie_jar.set("pgv_pvi", "xxx", domain=".qq.com")
cookie_jar.set("uin", "xxx", domain=".qq.com")
cookie_jar.set("pgv_si", "xxx", domain=".qq.com")
cookie_jar.set("skey", "xxx", domain=".qq.com")
cookie_jar.set("_qpsvr_localtk", "xxx", domain=".qq.com")
cookie_jar.set("ptisp", "xxx", domain=".qq.com")
cookie_jar.set("RK", "xxx", domain=".qq.com")
cookie_jar.set("ptcz", "xxx", domain=".qq.com")

cookie_jar.set("p_uin", "xxx", domain=".egame.qq.com")
cookie_jar.set("pt4_token", "xxx", domain=".egame.qq.com")
cookie_jar.set("p_skey", "xxx", domain=".egame.qq.com")
cookie_jar.set("pgg_pvid", "xxx", domain=".egame.qq.com")
cookie_jar.set("pgg_ssid", "xxx", domain=".egame.qq.com")

res = requests.get(url, cookies=cookie_jar)
print(res.text)
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-315b23d8d28a024f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######计时器
~~~
import time as t


class MyTimer():

    def __init__(self):
        self.unit = ['年', '月', '天', '小时', '分钟', '秒']
        self.prompt = "未开始计时。。。"
        self.lasted = []
        self.begin = 0
        self.end = 0

    def __str__(self):
        return self.prompt

    __repr = __str__

    def __add__(self, other):
        prompt = "总共运行了"
        result = []
        for index in range(6):
            result.append(self.lasted[index] + other.lasted[index])
            if result[index]:
                prompt += (str(result[index]) + self.unit[index])
        return prompt

    # 开始计时
    def start(self):
        self.begin = t.localtime()
        self.prompt = "提示:请先调用stop()停止计时"
        print("计时开始。。。")

    # 停止计时
    def stop(self):
        if not self.begin:
            print("提示:请先调用start()进行计时")
        else:
            self.end = t.localtime()
            self._calc()
            print("计时结束。。。")

    ##内部方法，计算运行时间
    def _calc(self):
        self.lasted = []
        self.prompt = "总共运行了"
        for index in range(6):
            self.lasted.append(self.end[index] - self.begin[index])
            if self.lasted[index]:
                self.prompt += (str(self.lasted[index]) + self.unit[index])

        print(self.prompt)

if __name__ == '__main__':
    myTimer = MyTimer()
    myTimer.start()

    for i in list(range(0,1000000)):
        print(i)
    myTimer.stop()

~~~

~~~
其他类使用：
import MyTimer

myTimer = MyTimer.MyTimer()
myTimer.start()


。。。。

myTimer.stop()
~~~
