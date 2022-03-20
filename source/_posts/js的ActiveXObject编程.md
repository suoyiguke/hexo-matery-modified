---
title: js的ActiveXObject编程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: js
categories: js
---
---
title: js的ActiveXObject编程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: js
categories: js
---
ActiveXObject只有IE支持

1、读取文件
~~~

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    
    <script>
        var fso = new ActiveXObject('Scripting.FileSystemObject');
        var f1 = fso.GetFile('C:/Users/yinkai/Desktop/工作情况.txt');
        alert('File last modified: ' + f1.DateLastModified);
        
    </script>
</head>
<body>

</body>
</html>
~~~
