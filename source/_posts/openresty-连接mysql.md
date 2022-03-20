---
title: openresty-连接mysql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: openresty
categories: openresty
---
---
title: openresty-连接mysql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: openresty
categories: openresty
---
###数据准备
~~~
CREATE TABLE `lua_test`.`user`  (
  `id` int(11) NOT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `age` int(3) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

INSERT INTO `lua_test`.`user`(`id`, `username`, `password`, `age`) VALUES (1, 'yk', '123', 22);
INSERT INTO `lua_test`.`user`(`id`, `username`, `password`, `age`) VALUES (2, '蓑衣孤客', '321', 21);
INSERT INTO `lua_test`.`user`(`id`, `username`, `password`, `age`) VALUES (3, 'coder', 'fff', 3123);

~~~

###

### lua代码
~~~

local mysql = require("resty.mysql")


--创建mysql连接实例
local db, err = mysql:new()
if not db then
    ngx.say("new mysql error : ", err)
    return
end
--设置超时时间(毫秒)
db:set_timeout(1000)

-- 定义链接属性
local props = {
    host = "127.0.0.1",
    port = 3306,
    database = "lua_test",
    user = "root",
    password = "yk123"
}

-- 发起连接
local res, err, errno, sqlstate = db:connect(props)

if not res then
    ngx.say("connect to mysql error : ", err, " , errno : ", errno, " , sqlstate : ", sqlstate)
    return close_db(db)
end



--查询
local select_sql = "SELECT * FROM `user`"
res, err, errno, sqlstate = db:query(select_sql)
if not res then
    ngx.say("select error : ", err, " , errno : ", errno, " , sqlstate : ", sqlstate)
    return close_db(db)
end

-- 结果集处理
list = {}
for i, row in ipairs(res) do
    table.insert(list,row)
end

--输出 json
local cjson = require("cjson")
local str = cjson.encode(list)
ngx.say(str)


-- 关闭mysql链接
local function close_db(db)
    if not db then
        return
    end
    db:close()
end

close_db(db)
~~~

###nginx.conf
~~~
  location /content_by_lua  {
    default_type 'text/html';
    content_by_lua_file E:\lua\Openresty_For_Windows_1.13.5.1001_64Bit\x64\lua_test\script\db.lua;
  }
~~~

###访问
![image.png](https://upload-images.jianshu.io/upload_images/13965490-64b1bc88d2489d06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
