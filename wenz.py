import os
fileList = os.listdir("E:\web\hexo-matery-modified\source\_posts")
fList=[]
for file in fileList:
   md = os.path.splitext(file);
   if md[1] =='.md':
       fList.append(file)
       print(file)


title = open('title',encoding='UTF-8')  # 打开文件
contentTitle = title.read();
print(contentTitle)

print(fList)
for f in fList:
    contentTitleSrc=contentTitle.format(title=f)
    with open("E:\web\hexo-matery-modified\source\_posts\\"+f, 'r+',encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(contentTitleSrc + content)
