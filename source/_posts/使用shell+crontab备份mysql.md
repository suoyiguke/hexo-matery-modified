---
title: 使用shell+crontab备份mysql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: shell
categories: shell
---
---
title: 使用shell+crontab备份mysql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: shell
categories: shell
---
1、先在机器上安装mysqldump
单独安装mysqldump
~~~
yum -y install holland-mysqldump.noarch
~~~

2、编写备份mysql的shell脚本
vi mysql_backup.sh
~~~
#!/usr/bin/env bash
#备份文件存储的目录
BACKUP_DIR=/data/docker/mysql/slave/backup

#以执行的日期作为文件名，以防文件名重复覆盖
DATE=$(date +%Y_%m_%d)


#用户名
MYSQL_USER=root

#密码
MYSQL_PWD=root

#IP
HOST=192.168.10.11

#PORT
PORT=33066

#使用的数据库
DATABASE=test

echo "mysql backup start $DATE"
#判断一下如果备份的目录不存在，就创建该目录
if [ ! -d $BACKUP_DIR/$DATE ]
then mkdir -p $BACKUP_DIR/$DATE
fi

#执行mysql备份数据库指令
mysqldump -u$MYSQL_USER -p$MYSQL_PWD --host=$HOST --port=$PORT $DATABASE | gzip > $BACKUP_DIR/$DATE/$DATE.sql.gz


#删除5天前的老的备份
find $BACKUP_DIR -mtime +5 -name "*.gz" -exec rm -rf {} \;

#解释上面这行命令的含义：
#find 是找到命令，找到变量BACKUP_DIR目录下 时间(-mtime) 5天前(+5) ，名字是(-name) 以.sql结尾的("*.sql")
#如果找到了的话(-exec),就执行后面的命令，rm -rf 删除 , {} \ 就是找到的内容。

~~~


3、使用linux上的定时任务框架crontab 
使用crontab -e 编辑
~~~
* * * * * bash /data/docker/mysql/slave/mysql_backup.sh > /tmp/load.log 2>&1 &
~~~
保存后重启服务
~~~
systemctl restart crond 
~~~
