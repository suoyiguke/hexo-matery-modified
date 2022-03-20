import os

fileList = os.listdir("C:\\Users\\yinkai\\Desktop\\新建文件夹")
fList = []
dict = {}
for file in fileList:
    list = os.listdir("C:\\Users\\yinkai\\Desktop\\新建文件夹\\" + file)
    dict[file] = list

print(dict)


title = open('title', encoding='UTF-8')  # 打开文件
contentTitle = title.read();
print(contentTitle)

fileList =[]
for key,fList in  dict.items():
    for title in fList:
        contentTitleSrc = contentTitle.format(title=title,tags=key,categories=key)
        fileSrc = "C:\\Users\\yinkai\\Desktop\\新建文件夹\\"+key+"\\" + title
        fileList.append(fileSrc)
        with open(fileSrc,'r+', encoding='UTF-8')  as f:
            try:
             content = f.read()
            except Exception as e:
                print(fileSrc)
            f.seek(0, 0)
            f.write(contentTitleSrc + content)

import shutil
for file  in fileList:
  shutil.copy(file, 'E:\web\hexo-matery-modified\source\_posts\\')
