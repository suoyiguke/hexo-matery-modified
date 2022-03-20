---
title: tesserocr-验证码识别.md
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
title: tesserocr-验证码识别.md
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
tesserocr
1、python驱动下载
https://github.com/simonflueckiger/tesserocr-windows_build

2、https://github.com/UB-Mannheim/tesseract/wiki 下载Tesseract_OCR

3、调用代码
~~~
import tesserocr
from PIL import Image
image = Image.open(r'C:\Users\yinkai\Desktop\v2-2fc0d12d2ff98b0bbe4e8af5ee589a22_720w.jpg')
print(tesserocr.image_to_text(i
~~~
~~~
import tesserocr
print(tesserocr.file_to_text(r'C:\Users\yinkai\Desktop\v2-2fc0d12d2ff98b0bbe4e8af5ee589a22_720w.jpg'))
~~~

4、报错
Traceback (most recent call last):
  File "C:/Users/yinkai/PycharmProjects/bankData/main.py", line 4, in <module>
    print(tesserocr.image_to_text(image))
  File "tesserocr.pyx", line 2555, in tesserocr._tesserocr.image_to_text
RuntimeError: Failed to init API, possibly an invalid tessdata path: D:\python/tessdata/

解决：将安装Tesseract_OCR生成的tessdata目录复制到 D:\python/tessdata/
