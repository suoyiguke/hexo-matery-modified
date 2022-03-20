---
title: selenium-抓取数据实例1.md
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
title: selenium-抓取数据实例1.md
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
~~~
import json
import locale
import tkinter as tk
import tkinter.messagebox
import uuid
from telnetlib import EC
import tkinter.messagebox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time;


def method_name():
    try:
        global geinput_str
        soup = BeautifulSoup(browser.page_source, 'lxml')
        geinput_str = soup.select('[placeholder="图形验证码"]')
        va = geinput_str[0]
        value = va.attrs['value']
        return value
    except:
        return


def run(browser, createdBefore, createdAfter, pageSize, time=None):
    # 保存到本地excel
    filename = time.strftime("%Y%d%d", time.localtime(time.time())) + ''.join(str(uuid.uuid1()).split('-')) + ".xlsx"
    browser.get("https://mall-sop.cgbchina.com.cn/")
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'name'))).send_keys("")
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys("")
    while not method_name():
        tk.messagebox.showinfo('提示', '请手动输入验证码，输入完点确定！注意不要自己点登录！')
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='ant-btn login-button ant-btn-primary ant-btn-lg ant-btn-two-chinese-chars']"))).click()
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-menu-submenu-title'))).click()
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="ant-menu-item menu-item"]'))).click()
    browser.get(
        'https://t?pageSize={pageSize}&createdAfter={createdAfter}&createdBefore={createdBefore}&pageNo={pageNo}'.format(
            pageSize=pageSize, createdBefore=createdBefore, createdAfter=createdAfter, pageNo=(str(1))))
    ele = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-total-text')))
    globalSoup = BeautifulSoup(browser.page_source, 'lxml')
    pageCount = 0
    # 总页数
    xh = globalSoup.select("li[title='向后 5 页']")
    if xh:
        xhf = xh[0].next_sibling
        pageCountStr = xhf.attrs['title']
        pageCount = int(pageCountStr)
    else:
        xh = globalSoup.select("li[title='下一页']")
        if xh:
            xhf = xh[0].previous_sibling
            pageCountStr = xhf.attrs['title']
            pageCount = int(pageCountStr)
    print("页大小：" + str(pageSize))
    print("总页数：" + str(pageCount))
    print("总订单数：" + str(ele))
    print("filename：" + filename)
    dataList = []
    for i in list(range(0, pageCount)):
        num = i + 1
        print("正在抓取第" + str(num) + '页...')
        browser.get(
            'https://?pageSize={pageSize}&createdAfter={createdAfter}&createdBefore={createdBefore}&pageNo={pageNo}'.format(
                pageSize=pageSize, createdBefore=createdBefore, createdAfter=createdAfter, pageNo=(str(num))))
        # 等待加载
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-total-text')))

        mySoup = BeautifulSoup(browser.page_source, 'lxml')
        webList = mySoup.select(".order-item")
        for item in webList:
            dList = []
            ddbh = ''
            name = ''
            ddh = ''
            jg = ''
            num = ''
            try:
                span = item.select('div[class="ant-col ant-col-21"] > span')
                # 下单时间
                time = span[0].text[4:]
                # 订单编号
                ddbh = item.select('a[class="active-link"]')[0].text
                # 价格
                jg = item.select('span[class="currency"]')[0].text
                num = item.select('div[class="ant-col ant-col-3"] > span')[0].text[1:]
                # 名称
                name = item.select('a[class="inactive-link cutwords-3-line"]')[0].text
                # 订单行ID:47708693284
                ddh = item.select('div[class="sku-attr"]')[1].text[6:]

                # 在表中写入相应的数据
                dList.append(time)
                dList.append(ddbh)
                dList.append(jg)
                dList.append(num)
                dList.append(name)
                dList.append(ddh)
                dataList.append(dList)
            except:
                print('异常' + item)
    try:
        df = pd.DataFrame(dataList, columns=['下单时间', '订单编号', '结算价格', '数量', '商品标题', '订单行ID'])
        df.to_excel(filename, index=False)
        print('抓取完成,本次抓取' + str(len(dataList)) + '条订单')
    except Exception as e:
        print('--- the error is ---:', e)
    finally:
        browser.quit()
        print(json.dumps(dataList))


if __name__ == '__main__':
    try:
        # 设置中文locale
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        tip = tkinter.Tk()
        # 隐藏主窗口
        # tip.withdraw()
        browser = webdriver.Chrome()
        # 隐式等待10秒。响应式等待优先级比它高。这里作为兜底。如果不加可能就出现因为找不到元素报错退出
        browser.implicitly_wait(10)
        pageSize = 500
        createdBefore = '2022-01-31 23:59:59'
        createdAfter = '2022-01-01 00:00:00'
        run(browser, createdBefore, createdAfter, pageSize, time)
    except Exception as e:
        print('--- the error is ---:', e)
    finally:
        # 如果不销毁浏览器实例，那么程序很难退出
        browser.quit()
        tip.destroy()

~~~

第二版，加上校验的
~~~
import json
import locale
import re
import tkinter as tk
import tkinter.messagebox
import uuid
from telnetlib import EC
import tkinter.messagebox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time;
import traceback


def vali(list, i):
    if list:
        if i or i == 0:
            size = len(list)
            if size == 0:
                return False
            elif size - 1 >= i:
                return True

    return False


def method_name():
    try:
        global geinput_str
        soup = BeautifulSoup(browser.page_source, 'lxml')
        geinput_str = soup.select('[placeholder="图形验证码"]')
        va = geinput_str[0]
        value = va.attrs['value']
        return value
    except:
        return


def run(browser, createdBefore, createdAfter, pageSize, time=None):
    # 保存到本地excel
    filename = time.strftime("%Y%d%d", time.localtime(time.time())) + ''.join(str(uuid.uuid1()).split('-')) + ".xlsx"
    login(browser)
    browser.get(
        'https://mall-sop.cgbchina.com.cn/orders/point?pageSize={pageSize}&createdAfter={createdAfter}&createdBefore={createdBefore}&pageNo={pageNo}&status=200'.format(
            pageSize=pageSize, createdBefore=createdBefore, createdAfter=createdAfter, pageNo=(str(1))))
    ele = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-total-text')))
    globalSoup = BeautifulSoup(browser.page_source, 'lxml')
    pageCount = 0
    # 总页数
    xh = globalSoup.select("li[title='向后 5 页']")
    if xh:
        xhf = xh[0].next_sibling
        pageCountStr = xhf.attrs['title']
        pageCount = int(pageCountStr)
    else:
        xh = globalSoup.select("li[title='下一页']")
        if xh:
            xhf = xh[0].previous_sibling
            pageCountStr = xhf.attrs['title']
            pageCount = int(pageCountStr)
    print("页大小：" + str(pageSize))
    print("总页数：" + str(pageCount))
    print("总订单数：" + str(ele))
    print("filename：" + filename)
    dataList = []
    for i in list(range(0, pageCount)):
        num = i + 1
        print("正在抓取第" + str(num) + '页...')
        browser.get(
            'https://mall-sop.cgbchina.com.cn/orders/point?pageSize={pageSize}&createdAfter={createdAfter}&createdBefore={createdBefore}&pageNo={pageNo}&status=200'.format(
                pageSize=pageSize, createdBefore=createdBefore, createdAfter=createdAfter, pageNo=(str(num))))
        # 等待加载
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-total-text')))

        mySoup = BeautifulSoup(browser.page_source, 'lxml')
        webList = mySoup.select(".order-item")
        for item in webList:
            dList = []
            orderNo = '无'
            prodcutName = '无'
            try:
                # 订单编号
                orderNoSo = item.select_one('a[class="active-link"]')
                if orderNoSo:
                    orderNo = orderNoSo.text

                # 名称
                prodcutNameSo = item.select_one('a[class="inactive-link cutwords-3-line"]')
                if prodcutNameSo:
                    prodcutName = prodcutNameSo.text

                # 在表中写入相应的数据
                dList.append(orderNo)

                spanv = '无'
                span = item.select_one('div[class="ant-col ant-col-21"] > span')
                if span:
                    spanv = span.text[4:]  # 下单时间

                dList.append(spanv)

                # 订单行ID:47708693284
                ddh = item.select('div[class="sku-attr"]')
                ddhv = '无'
                if ddh:
                    if vali(ddh, 1):
                        ddhv = item.select('div[class="sku-attr"]')[1].text[6:]
                dList.append(ddhv)

                getDetail(browser, orderNo, dList, prodcutName)
                dataList.append(dList)
            except Exception as e:
                traceback.print_exc()
    try:
        df = pd.DataFrame(dataList,
                          columns=['订单编号', '创建时间', '订单行ID', '客户名称', '客户手机号', '收货地址',
                                   '买家留言', '订单状态', '商品名称', '商品编码', '清算单价',
                                   '单价积分', '单价现金', '兑换数量', '总价积分', '总价现金'])
        df.to_excel(filename, index=False)
        print('抓取完成,本次抓取' + str(len(dataList)) + '条订单')
    except Exception as e:
        traceback.print_exc()
        # 或者得到堆栈字符串信息
    finally:
        browser.quit()
        print(json.dumps(dataList))


def login(browser):
    browser.get("https://")
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'name'))).send_keys("")
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys("")
    while not method_name():
        tk.messagebox.showinfo('提示', '请手动输入验证码，输入完点确定！注意不要自己点登录！')
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                     "[class='ant-btn login-button ant-btn-primary ant-btn-lg ant-btn-two-chinese-chars']"))).click()
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-menu-submenu-title'))).click()
    WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="ant-menu-item menu-item"]'))).click()


### 抓取详情页
def getDetail(browser, orderNo, dList, prodcutName):
    if not orderNo:
        return
    try:
        browser.get("https://mall-sop.cgbchina.com.cn/order/detail/point/{orderNo}".format(orderNo=orderNo))
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr[class='ant-table-row ant-table-row-level-0']")))
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tbody[class='ant-table-tbody']>tr>td")))
        soup = BeautifulSoup(browser.page_source, 'lxml')
        divList = soup.select("div[class='ant-col ant-col-12']")
        t1 = '无'
        if divList:
            if vali(divList, 0):
                if vali(divList[0].contents, 1):
                    t1 = divList[0].contents[1]  # 客户名称
        dList.append(t1)

        t2 = '无'
        if divList:
            if vali(divList, 1):
                if vali(divList[1].contents, 1):
                    t2 = divList[1].contents[1]  # 客户手机号

        dList.append(t2)

        t3 = '无'
        if divList:
            if vali(divList, 2):
                if vali(divList[2].contents, 1):
                    t3 = divList[2].contents[1]  # 收货地址
        dList.append(t3)

        #
        t4 = '无'
        ly = soup.select_one("div[class='detail-basic']").select("div[class='basic-info']")[1]
        if ly:
            if vali(ly.contents, 3):
                if vali(ly.contents[3].contents, 1):
                    t4 = ly.contents[3].contents[1]  # 买家留言
        dList.append(t4)

        t5 = '无'
        f = soup.select_one("div[class='action-area']")
        #
        if f:
            if vali(f.contents, 0):
                if vali(f.contents[0].contents, 1):
                    t5 = f.contents[0].contents[1]  # 订单状态
        dList.append(t5)
        dList.append(prodcutName)  # 商品名称
        div = soup.select_one("tbody[class='ant-table-tbody']").find_all("td")

        #
        t6 = '无'
        t6v = soup.select_one("div[class='sku-attr']")
        if t6v:
            t6 = t6v.text
        dList.append(t6[5:])

        t7 = '无'
        if div:
            if vali(div, 1):
                t7 = div[1].text  # 清算单价(元)
        dList.append(t7)

        t8 = '无'
        t9 = '无'
        if div:
            if vali(div, 2):

                dan = re.findall("积分：(.+)、现金：(.+)", div[2].text)
                if dan:
                    if vali(dan, 0):
                        if vali(dan[0], 0):
                            t8 = dan[0][0]  # 兑换单积分
                        if vali(dan[0], 1):
                            t9 = dan[0][1]  # 兑换单价
        dList.append(t8)
        dList.append(t9)

        t10 = '无'
        if div:
            if vali(div, 3):
                t10 = div[3].text  # 兑换数量
        dList.append(t10)

        t11 = '无'
        t12 = '无'
        if div:
            if vali(div, 4):
                hipo = re.findall("积分:(.+)、现金:(.+)", div[4].text)
                if hipo:
                    if vali(hipo, 0):
                        if vali(hipo[0], 0):
                            t11 = hipo[0][0]  # 兑换单积分
                        if vali(hipo[0], 1):
                            t12 = hipo[0][1]  # 兑换单价
        dList.append(t11)
        dList.append(t12)


    except Exception as e:
        traceback.print_exc()
        # 或者得到堆栈字符串信息
        info = traceback.format_exc()

    # antList = soup.select('div[class="basic-info"] > .ant-row-flex')
    # dList.append(antList[0].contents[0].contents[1])  # 订单编号 47708641535
    # dList.append(antList[0].contents[1].contents[1])  # 创建时间 2022/01/31 20:38:15
    # dList.append(antList[0].contents[2].contents[1])  # 购买类型 一期
    # dList.append(antList[1].contents[0].contents[1])  # 下单渠道 手机银行APP
    # dList.append(antList[1].contents[1].contents[1])  # 商品类型 实物商品
    # dList.append(antList[1].contents[2].contents[1])  # 物流平台 其他
    # dList.append(antList[2].contents[0].contents[1])  # 交易平台 积分商城
    # dList.append(antList[2].contents[1].contents[1])  # 订单类型 普通订单



if __name__ == '__main__':
    try:
        # 设置中文locale
        locale.setlocale(locale.LC_CTYPE, 'chinese')
        tip = tkinter.Tk()
        # 隐藏主窗口
        # tip.withdraw()
        browser = webdriver.Chrome()
        # 隐式等待10秒。响应式等待优先级比它高。这里作为兜底。如果不加可能就出现因为找不到元素报错退出
        browser.implicitly_wait(10)
        pageSize = 5
        createdAfter = '2021/01/01 17:09:12'
        createdBefore = '2022/03/09 17:09:12'
        run(browser, createdBefore, createdAfter, pageSize, time)
    except Exception as e:
        traceback.print_exc()
        # 或者得到堆栈字符串信息
        info = traceback.format_exc()
    finally:
        # 如果不销毁浏览器实例，那么程序很难退出
        browser.quit()
        tip.destroy()

# import pandas as pd
#
# if __name__ == '__main__':
#     dataList =[["486810220741", "2022/03/09 17:09:12", "486810421454", "\u6c5f\u5c11\u7ea2 13534533722 \u5e7f\u4e1c\u7701\u63ed\u9633\u5e02\u66f2\u6eaa\u9547\u4e91\u5357\u6751\u65b0\u539d\u533a\u4e09\u5df720\u53f7   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["446610300400", "2022/03/09 17:08:52", "446610431365", "\u5218\u4e3d 15909208538 \u9655\u897f\u7701\u897f\u5b89\u5e02\u51e4\u57ce\u5341\u8def\u859b\u5bb6\u5be8\u5c0f\u533a\u4e00\u53f7\u697c\u4e00\u5355\u5143902   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["469710190848", "2022/03/09 17:08:18", "469710391559", "13483170068", "\u9ad8\u806a\u4e91 18134284277 \u6cb3\u5317\u7701\u77f3\u5bb6\u5e84\u5e02\u534f\u795e\u4e61\u7b14\u5934\u6751\uff11\uff11\u6392\uff11\u53f7   ", "\u65e0", "\u4e91\u67d4\u6297\u83cc\u9632\u87a8\u8212\u9002\u6795(\u4f4e\u6b3e/\u5355\u8fb9)"], ["430610290436", "2022/03/09 17:08:16", "430610471257", "18734928206", "\u5f20\u6587\u541b 18734928206  \u5c71\u897f\u7701                                               \u592a\u539f\u5e02                                               \u4e07\u67cf\u6797\u533a                                              \u4e07\u67cf\u6797\u8857\u9053                                            \u5c71\u897f\u7701\u592a\u539f\u5e02\u4e07\u67cf\u6797\u533a\u4e0a\u5e84\u8857\u4e0a\u5e84\u6613\u5c45\u65f6\u4ee3", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["429410240661", "2022/03/09 17:08:09", "429410401440", "15910666073", "\u97e9\u5ce5 15910666073 \u5317\u4eac\u5e02\u5317\u4eac\u5e02\uff08\u5e02\u8f96\u533a\uff09\u4ea6\u5e84\u4e07\u6e90\u885718\u53f7   ", "\u9500\u552e\u5927\u5385\u5e02\u573a\u529e\u516c\u5ba4", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["462010300397", "2022/03/09 17:07:45", "462010431362", "18869999669", "\u9646\u5fb7\u666e 18869999669 \u6d59\u6c5f\u7701\u53f0\u5dde\u5e02\u5929\u53f0\u53bf\u98de\u9e64\u8def\u77f3\u6cb9\u516c\u53f8\uff13\u697c\uff13\uff10\uff16   ", "\u65e0", "\u4eac\u4e1c\u4eac\u9020\u4fbf\u643a\u6237\u5916\u8fd0\u52a8\u5927\u5bb9\u91cfTritan\u5851\u6599\u6c34\u58f61.9L"], ["436110260537", "2022/03/09 17:07:18", "436110451311", "15638758770", "\u738b\u8fdb\u73c2 15638758770 \u6cb3\u5357\u7701\u8bb8\u660c\u5e02\u97e9\u57ce\u8857\u9053\u5929\u6e90\u793e\u533a\u7535\u5382\u5bb6\u5c5e\u96622\u53f7\u9662   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["467210210757", "2022/03/09 17:07:02", "467210411469", "15887959468", "\u6731\u8d5b\u743c 15887959468 \u4e91\u5357\u7701\u66f2\u9756\u5e02\u6587\u534e\u8857\u9053\u4ee3\u6cb3\u5de5\u4e1a\u56ed\u533a\u95fd\u5357\u94dd\u5408\u91d1\u4e0d\u9508\u94a2\u94a2\u5e02\u573a12\u5e621\u53f7\u6d77\u8fd0\u4e0d\u9508  ", "\u65e0", "\u4e91\u67d4\u6297\u83cc\u9632\u87a8\u8212\u9002\u6795(\u4f4e\u6b3e/\u5355\u8fb9)"], ["426410230764", "2022/03/09 17:06:53", "426410361726", "13394632985", "\u4e8e\u5f3a 13394632985 \u9ed1\u9f99\u6c5f\u7701\u5927\u5e86\u5e02\u6052\u5927\u7eff\u6d32\uff17\u53f7\u697c\uff12\u5355\u5143\uff11\uff12\uff10\uff12   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["412810200758", "2022/03/09 17:06:47", "412810381535", "15258350345", "\u91d1\u8f89 15258350345 \u6d59\u6c5f\u7701\u5b81\u6ce2\u5e02\u6ca7\u6d77\u5357\u8def157\u53f7605   ", "\u65e0", "\u4eac\u4e1c\u4eac\u9020\u4fbf\u643a\u6237\u5916\u8fd0\u52a8\u5927\u5bb9\u91cfTritan\u5851\u6599\u6c34\u58f61.9L"], ["401310200757", "2022/03/09 17:06:20", "401310381534", "18949882656", "\u5f20\u8679 18949882656 \u5b89\u5fbd\u7701\u5408\u80a5\u5e02\u6708\u534e\u8def\u4e0e\u7687\u85cf\u88d5\u8def\u4ea4\u6c47\u5904\u897f\u5357\u89d2\u4e16\u7eaa\u8363\u5ef73\u671f  ", "\u65e0", "\u4eac\u4e1c\u4eac\u9020\u4fbf\u643a\u6237\u5916\u8fd0\u52a8\u5927\u5bb9\u91cfTritan\u5851\u6599\u6c34\u58f61.9L"], ["438410260534", "2022/03/09 17:06:12", "438410451308", "\u5f20\u57f9\u6587 13823585032 \u5e7f\u4e1c\u7701\u6df1\u5733\u5e02\u677e\u5c97\u7ea2\u661f\u683c\u5e03\u4e8c\u5df7\u5341\u4e94\u53f7\uff19\uff10\uff11\u5ba4   ", "\u65e0", "\u98d8\u67d4\u9999\u6c1b\u6d17\u53d1\u6c34/\u9732\u62a4\u53d1\u7d20\u6301\u4e45\u7559\u9999\u67d4\u987a\u5957\u88c5300g+300g"], ["430610220731", "2022/03/09 17:05:51", "430610421444", "18734928206", "\u5f20\u6587\u541b 18734928206 \u5c71\u897f\u7701\u592a\u539f\u5e02\u91d1\u9633\u8def\uff11\uff10\u53f7\u5c71\u897f\u516d\u5efa\u96c6\u56e2\u6709\u9650\u516c\u53f8\u5c71\u897f\u516d\u5efa\u96c6\u56e2\u6709\u9650\u516c\u53f8\u5de5\u7a0b\u90e8\uff5c\u9879\u76ee\u90e8  ", "\u65e0", "\u4eac\u4e1c\u4eac\u9020\u4fbf\u643a\u6237\u5916\u8fd0\u52a8\u5927\u5bb9\u91cfTritan\u5851\u6599\u6c34\u58f61.9L"], ["426110290426", "2022/03/09 17:05:42", "426110471247", "13926601300", "\u5218\u4e16\u5eb7 13926601300 \u5e7f\u4e1c\u7701\u6e05\u8fdc\u5e02\u5e7f\u6e05\u5927\u9053\u73b0\u4ee3\u57ce9\u680b2208   ", "\u65e0", "\u4eac\u4e1c\u4eac\u9020\u4fbf\u643a\u6237\u5916\u8fd0\u52a8\u5927\u5bb9\u91cfTritan\u5851\u6599\u6c34\u58f61.9L"], ["471610230752", "2022/03/09 17:05:42", "471610361714", "17798950022", "\u5b59\u6d01 17798950022 \u6c5f\u82cf\u7701\u626c\u5dde\u5e02\u6c5f\u82cf\u7701\u626c\u5dde\u5e02\u6052\u5927\u5e1d\u666f\u4e1c\u56ed\uff11\uff11\u680b\uff12\uff10\uff15\u5ba4   ", "\u65e0", "\u62dc\u5c14\u6210\u4eba\u58f0\u6ce2\u7535\u52a8\u7259\u5237"], ["467210210749", "2022/03/09 17:05:37", "467210411461", "15887959468", "\u6731\u8d5b\u743c 15887959468 \u4e91\u5357\u7701\u66f2\u9756\u5e02\u6587\u534e\u8857\u9053\u4ee3\u6cb3\u5de5\u4e1a\u56ed\u533a\u95fd\u5357\u94dd\u5408\u91d1\u4e0d\u9508\u94a2\u94a2\u5e02\u573a12\u5e621\u53f7\u6d77\u8fd0\u4e0d\u9508  ", "\u65e0", "\u4e91\u67d4\u6297\u83cc\u9632\u87a8\u8212\u9002\u6795(\u4f4e\u6b3e/\u5355\u8fb9)"], ["410910260530", "2022/03/09 17:05:08", "410910451304", "15011424003", "\u6768\u5c0f\u950b 15011424003 \u56db\u5ddd\u7701\u6210\u90fd\u5e02\u5c0f\u5357\u8857109\u53f7\u897f\u5e9c\u5c11\u57ce1\u680b1\u5355\u51431102   ", "\u65e0", "\u98de\u5229\u6d66 24W\u8f66\u8f7d\u5145\u7535\u5668"], ["475710260529", "2022/03/09 17:05:07", "475710451303", "13534565377", "\u9648\u5229 13534565377 \u5e7f\u4e1c\u7701\u4f5b\u5c71\u5e02\u987a\u5fb7\u533a\u5927\u826f\u9547\u4e91\u6842\u56db\u8857\u4e94\u5df713\u53f7501   ", "\u65e0", "\u98de\u5229\u6d66 24W\u8f66\u8f7d\u5145\u7535\u5668"], ["412410270455", "2022/03/09 17:04:50", "412410441226", "13760837766", "\u6c88\u5efa\u5174 13760837766 \u798f\u5efa\u7701\u8386\u7530\u5e02\u62f1\u8fb0\u8857\u9053\u4e07\u79d1\u57ce4\u671f   ", "\u65e0", "\u98d8\u67d4\u9999\u6c1b\u6d17\u53d1\u6c34/\u9732\u62a4\u53d1\u7d20\u6301\u4e45\u7559\u9999\u67d4\u987a\u5957\u88c5300g+300g"], ["447010300377", "2022/03/09 17:04:02", "447010431342", "17761600722", "\u8d75\u4e39 17761600722 \u6d59\u6c5f\u7701\u5b81\u6ce2\u5e02\u9f99\u5c71\u9547\u8fbe\u84ec\u6751\u4e09\u5317\u8def201\u5f0417\u53f7   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["434910260524", "2022/03/09 17:04:01", "434910451298", "18243080815", "\u738b\u5a1c\u514b\u7433 18243080815 \u5409\u6797\u7701\u957f\u6625\u5e02\u6c49\u53e3\u5c0f\u533a\u65b0\uff19\u680b\uff12\u5355\u5143\uff13\uff10\uff14\u5ba4   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["438010210737", "2022/03/09 17:03:25", "438010411449", "\u6f58\u6d77\u5e73 15992408830 \u5e7f\u4e1c\u7701\u5e7f\u5dde\u5e02\u5927\u6e90\u9ec4\u5e84\u5317\u8def28\u53f7\u5409\u5bb6\u516c\u5bd3   ", "\u65e0", "\u4eac\u4e1c\u4eac\u9020\u4fbf\u643a\u6237\u5916\u8fd0\u52a8\u5927\u5bb9\u91cfTritan\u5851\u6599\u6c34\u58f61.9L"], ["457810260521", "2022/03/09 17:03:25", "457810451295", "\u738b\u6625\u91ce 18746854777 \u4e91\u5357\u7701\u6606\u660e\u5e02\u6606\u660e\u5e02\u5b98\u6e21\u533a\u5927\u677f\u6865\u8857\u9053\u957f\u6c34\u822a\u57ce\u6728\u85e4\u82d1\u5546\u94fa\u4e1c\u5317\u5bb6\u5e38\u83dc  ", "\u65e0", "\u98d8\u67d4\u9999\u6c1b\u6d17\u53d1\u6c34/\u9732\u62a4\u53d1\u7d20\u6301\u4e45\u7559\u9999\u67d4\u987a\u5957\u88c5300g+300g"], ["440710200740", "2022/03/09 17:03:05", "440710381517", "18092159812", "\u738b\u7f8e\u971e 18092159812 \u9655\u897f\u7701\u897f\u5b89\u5e02\u4e08\u516b\u516d\u8def\u9ad8\u65b0\u9038\u54c1\uff13\uff0d\uff11\uff0d\uff11\uff19\uff10\uff13   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["452710200738", "2022/03/09 17:02:46", "452710381515", "13927447768", "\u5434\u6620\u53f6 13927447768 \u5e7f\u4e1c\u7701\u6df1\u5733\u5e02\u6c99\u4e95\u8857\u9053\u6865\u5934\u8354\u56ed\u8def\u8354\u56ed\u5c0f\u533a\uff22\u680b\uff11\uff10\uff10\uff13   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["462310280459", "2022/03/09 17:02:45", "462310461239", "18638981011", "\u6731\u6e90\u6167 18638981011 \u6cb3\u5357\u7701\u5357\u9633\u5e02\u5367\u9f99\u533a\u5317\u4eac\u5927\u9053\u4e0e\u4e2d\u8fbe\u8def\u4ea4\u53c9\u53e3\u897f\u65bd\u5170\u82b1\u56ed   ", "\u65e0", "\u9738\u738b\u80b2\u53d1\u6db2\u5934\u53d1\u589e\u957f\u6db2\u6ecb\u517b\u5934\u76ae\u62a4\u7406\u7cbe\u534e\u6db260ml"], ["425010200734", "2022/03/09 17:02:33", "425010381511", "13776651322", "\u5f20\u5170\u5170 13776651322 \u6c5f\u82cf\u7701\u5357\u4eac\u5e02\u5357\u4eac\u5e02\u6c5f\u5b81\u533a\u6021\u666f\u56ed16\u680b1204\u5ba4   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["496010210730", "2022/03/09 17:02:24", "496010411442", "13537148832", "\u9648\u6653\u71d5 13537148832 \u5e7f\u4e1c\u7701\u4e1c\u839e\u5e02\u4e1c\u839e\u5e02\u5357\u57ce\u533a\u666f\u6e56\u65f6\u4ee3\u57ce17\u680b1\u5355\u51433002   ", "\u65e0", "\u82cf\u6cca\u5c14\u4e0d\u9508\u94a2\u5976\u9505ST16H1"], ["441510300362", "2022/03/09 17:01:40", "441510431327", "18764762657", "\u5f20\u6b23\u6b23 18764762657 \u5c71\u4e1c\u7701\u6d4e\u5b81\u5e02\u5c71\u4e1c\u7701\u6d4e\u5b81\u5e02\u9ad8\u65b0\u533a\u6d38\u6cb3\u8857\u9053\u897f\u95f8\u793e\u533a1\u53f7\u697c\u4e09\u5355\u51436\u697c\u4e1c  ", "\u65e0", "\u4e91\u67d4\u6297\u83cc\u9632\u87a8\u8212\u9002\u6795(\u4f4e\u6b3e/\u5355\u8fb9)"], ["478810230735", "2022/03/09 17:01:34", "478810361697", "17304467520", "\u5ed6\u5929\u4f26 17304467520 \u5e7f\u4e1c\u7701\u6df1\u5733\u5e02\u9f99\u6d77\u5bb6\u56ed1\u680bB2515   ", "\u65e0", "\u98de\u5229\u6d66 24W\u8f66\u8f7d\u5145\u7535\u5668"], ["410410190813", "2022/03/09 17:00:43", "410410391524", "13542776993", "\u6e29\u5efa\u5fe0 13542776993 \u5e7f\u4e1c\u7701\u60e0\u5dde\u5e02\u535a\u7f57\u53bf\u5546\u4e1a\u4e1c\u8857\u6021\u68ee\u82d1A2\u680b803   ", "\u65e0", "\u4e91\u67d4\u6297\u83cc\u9632\u87a8\u8212\u9002\u6795(\u4f4e\u6b3e/\u5355\u8fb9)"], ["485210300339", "2022/03/09 16:42:31", "485210431304", "15803702300", "\u6731\u6587\u51ef 15803702300 \u6cb3\u5357\u7701\u5546\u4e18\u5e02\u7762\u9633\u533a\u5b8b\u57ce\u897f\u8def\u51e4\u51f0\u6e7e\u5c0f\u533a", "\u65e0", "\uff08CC\u4e13\u7528\uff09\u62dc\u5c14\u6210\u4eba\u58f0\u6ce2\u7535\u52a8\u7259\u5237X1S+plus\u7c89\u8272\uff08\u53d1\u73b0\u7cbe\u5f69\uff09"], ["437310290352", "2022/03/09 16:33:47", "437310471171", "18657966182", "\u738b\u5fe0\u57f9 18657966182 \u6d59\u6c5f\u7701\u91d1\u534e\u5e02\u4e66\u9662\u8def\uff13\uff14\uff19\u53f7   ", "\u65e0", "\u9738\u738b\u80b2\u53d1\u6db2\u5934\u53d1\u589e\u957f\u6db2\u6ecb\u517b\u5934\u76ae\u62a4\u7406\u7cbe\u534e\u6db260ml"], ["497810210665", "2022/03/09 16:30:17", "497810411375", "18599335388", "\u60e0\u6587\u6d9b 18599335388 \u65b0\u7586\u7ef4\u543e\u5c14\u81ea\u6cbb\u533a\u660c\u5409\u56de\u65cf\u81ea\u6cbb\u5dde\u5317\u4eac\u5357\u8def189\u53f7\u7279\u53d8\u7535\u5de5\u603b\u90e84\u697c   ", "\u65e0", "\u9738\u738b\u80b2\u53d1\u6db2\u5934\u53d1\u589e\u957f\u6db2\u6ecb\u517b\u5934\u76ae\u62a4\u7406\u7cbe\u534e\u6db260ml"], ["497810260447", "2022/03/09 16:28:14", "497810451220", "18599335388", "\u60e0\u6587\u6d9b 18599335388 \u65b0\u7586\u7ef4\u543e\u5c14\u81ea\u6cbb\u533a\u660c\u5409\u56de\u65cf\u81ea\u6cbb\u5dde\u5317\u4eac\u5357\u8def189\u53f7\u7279\u53d8\u7535\u5de5\u603b\u90e84\u697c   ", "\u65e0", "\u9738\u738b\u80b2\u53d1\u6db2\u5934\u53d1\u589e\u957f\u6db2\u6ecb\u517b\u5934\u76ae\u62a4\u7406\u7cbe\u534e\u6db260ml"], ["457210240575", "2022/03/09 16:20:47", "457210401354", "13422079820", "\u9676\u5c71 13422079820 \u5e7f\u4e1c\u7701\u5e7f\u5dde\u5e02\u949f\u6751\u8857105\u56fd\u9053\u96c4\u5cf0\u57ce\u6c83\u5c14\u739b\u4e00\u697c\u670d\u52a1\u53f0   ", "\u65e0", "\u9738\u738b\u80b2\u53d1\u6db2\u5934\u53d1\u589e\u957f\u6db2\u6ecb\u517b\u5934\u76ae\u62a4\u7406\u7cbe\u534e\u6db260ml"]]
#     df = pd.DataFrame(dataList,
#                       columns=['订单编号', '创建时间', '订单行ID', '客户名称', '客户手机号', '收货地址',
#                                '买家留言', '订单状态', '商品名称', '商品编码', '清算单价',
#                                '单价积分', '单价现金', '兑换数量', '总价积分', '总价现金'])
#     df.to_excel("xx.xlsx", index=False)
#     print('抓取完成,本次抓取' + str(len(dataList)) + '条订单')


~~~
