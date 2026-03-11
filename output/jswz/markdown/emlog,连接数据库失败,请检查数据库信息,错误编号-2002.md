---
title: "emlog,连接数据库失败,请检查数据库信息,错误编号 2002"
source: https://mrxn.net/jswz/emlog-mysql-2002error-solved.html
asset_dir: assets/emlog,连接数据库失败,请检查数据库信息,错误编号-2002
---

# emlog,连接数据库失败,请检查数据库信息,错误编号 2002

[Mrxn](https://mrxn.net/author/1)- 发表于2017/12/24 11:19
- 7555浏览
- [4评论](#comment)
- 53分钟阅读

深入探索

Web安全课程

Windows安全工具

文件大小转换

---

今天起来发现博客打不开了，提示：连接数据库失败,请检查数据库信息,错误编号 2002。

技术文章订阅

首先看这个错误代码是2002，并不是emlog的配置文件有问题，因为从include/lib/mysql.php里面可以看到这个2002应该是MySQL本身出问题了，但是不一定，下面来排查是不是MySQL本身出问题了。

`/**  
 * 内部实例对象  
 * @var object MySql  
 */  
 private static $instance = null;  
 private function __construct() {  
 if (!function_exists('mysql_connect')) {  
 emMsg('服务器空间PHP不支持MySql数据库');  
 }  
 if (!$this->conn = @mysql_connect(DB_HOST, DB_USER, DB_PASSWD)) {  
 switch ($this->geterrno()) {  
 case 2005:  
 emMsg("连接数据库失败，数据库地址错误或者数据库服务器不可用");  
 break;  
 case 2003:  
 emMsg("连接数据库失败，数据库端口错误");  
 break;  
 case 2006:  
 emMsg("连接数据库失败，数据库服务器不可用");  
 break;  
 case 1045:  
 emMsg("连接数据库失败，数据库用户名或密码错误");  
 break;  
 default :  
 emMsg("连接数据库失败，请检查数据库信息。错误编号：" . $this->geterrno());  
 break;  
 }  
 }  
 if ($this->getMysqlVersion() > '4.1') {  
 mysql_query("SET NAMES 'utf8'");  
 }  
 @mysql_select_db(DB_NAME, $this->conn) OR emMsg("连接数据库失败，未找到您填写的数据库");  
 }`

深入探索

安全研究工具

物流软件安全

软件

登上服务器，准备登录mysql，mysql -uroot -ppassword，报错如下：

编程

ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)

然后查看MySQL状态：

`root@mrxn:/# service mysqld status`  
`● mysqld.service - LSB: start and stop MySQL`  
 `Loaded: loaded (/etc/init.d/mysqld)`  
 `Active: active (exited) since Sun 2017-12-24 10:55:03 CST; 5min ago`  
 `Process: 536 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)`

`Dec 24 10:55:03 mrxn.guest mysqld[536]: Starting MySQL`  
`Dec 24 10:55:03 mrxn.guest mysqld[536]: Couldn't find MySQL server (/usr/bin/mysqld_safe) ... failed!`  
`Dec 24 10:55:03 mrxn.guest systemd[1]: Started LSB: start and stop MySQL.`

注意看红色的部分，Couldn't find MySQL server (/usr/bin/mysqld\_safe) ... failed! 现在可以进一步确定是MySQL本身出问题了。

问题原因就这与MySQL本身没有启动起来。我们先停止MySQL试试：service mysqld stop ，然后查看状态：

深入探索

数据库

网络安全课程

编程语言教程

`root@mrxn:/# service mysqld status`  
`● mysqld.service - LSB: start and stop MySQL`  
 `Loaded: loaded (/etc/init.d/mysqld)`  
 `Active: inactive (dead) since Sun 2017-12-24 11:01:09 CST; 1s ago`  
 `Process: 1809 ExecStop=/etc/init.d/mysqld stop (code=exited, status=0/SUCCESS)`  
 `Process: 536 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)`

`Dec 24 10:55:03 mrxn.guest mysqld[536]: Starting MySQL`  
`Dec 24 10:55:03 mrxn.guest mysqld[536]: Couldn't find MySQL server (/usr/bin/mysqld_safe) ... failed!`  
`Dec 24 10:55:03 mrxn.guest systemd[1]: Started LSB: start and stop MySQL.`  
`Dec 24 11:01:09 mrxn.guest systemd[1]: Stopping LSB: start and stop MySQL...`  
`Dec 24 11:01:09 mrxn.guest mysqld[1809]: MySQL server PID file could not be found! ... failed!`  
`Dec 24 11:01:09 mrxn.guest systemd[1]: Stopped LSB: start and stop MySQL.`

然后Google搜索上面的红色关键词：Couldn't find MySQL server (/usr/bin/mysqld\_safe) ... failed! ，借鉴这个的方法 <http://www.cnblogs.com/olinux/p/5546371.html>

搜索引擎

查看MySQL的my.cnf 在那些位置存在：

`root@mrxn:/# mysqld --verbose --help|grep my.cnf`  
`2017-12-24 11:02:32 0 [Warning] Using unique option prefix key_buffer instead of key_buffer_size is deprecated and will be removed in a future release. Please use the full name instead.`  
`2017-12-24 11:02:32 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled`  
`2017-12-24 11:02:32 0 [Note] mysqld (mysqld 5.6.37-log) starting as process 1867 ...`  
`2017-12-24 11:02:32 1867 [ERROR] Can't find messagefile '/usr/share/mysql/errmsg.sys'`  
`2017-12-24 11:02:32 1867 [Warning] Can't create test file /var/lib/mysql/mrxn.lower-test`  
`2017-12-24 11:02:32 1867 [Warning] Can't create test file /var/lib/mysql/mrxn.lower-test`  
`mysqld: Can't change dir to '/var/lib/mysql/' (Errcode: 2 - No such file or directory)`  
`2017-12-24 11:02:32 1867 [Warning] Using unique option prefix myisam-recover instead of myisam-recover-options is deprecated and will be removed in a future release. Please use the full name instead.`  
`2017-12-24 11:02:32 1867 [Note] Plugin 'FEDERATED' is disabled.`  
`mysqld: Unknown error 1146`  
`2017-12-24 11:02:32 1867 [ERROR] Can't open the mysql.plugin table. Please run mysql_upgrade to create it.`  
`/etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf`   
 `my.cnf, $MYSQL_TCP_PORT, /etc/services, built-in default`  
`2017-12-24 11:02:32 1867 [Note] Binlog end`  
`2017-12-24 11:02:32 1867 [Note] Shutting down plugin 'CSV'`  
`2017-12-24 11:02:32 1867 [Note] Shutting down plugin 'MyISAM'`

注意看红色的标注部分，没有那个文件或者路径。用ls -l /var/lib/ 查看下面确实没有mysql文件夹。

编程

那么就新建一个mysql文件夹，并且设置好权限给mysql使用：

`mkdir /var/lib/mysql/`

`chown -R mysql:mysql /var/lib/mysql/`

然后删除多余的那个my.cnf ：rm /etc/mysql/my.cnf

然后重启MySQL：service mysqld restart ，并且查看MySQL的状态:

`root@mrxn:/# service mysqld restart`  
`root@mrxn:/# service mysqld status`   
`● mysqld.service - LSB: start and stop MySQL`  
 `Loaded: loaded (/etc/init.d/mysqld)`  
 `Active: active (running) since Sun 2017-12-24 11:09:00 CST; 5s ago`  
 `Process: 2121 ExecStop=/etc/init.d/mysqld stop (code=exited, status=0/SUCCESS)`  
 `Process: 2138 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)`  
 `CGroup: /system.slice/mysqld.service`  
 `├─2153 /bin/sh /usr/local/mysql/bin/mysqld_safe --datadir=/data/mysql --pid-file=/data/mysql/mysql.pid`  
 `└─2992 /usr/local/mysql/bin/mysqld --basedir=/usr/local/mysql --datadir=/data/mysql --plugin-dir=/usr/local/mysql/l...`

`Dec 24 11:08:59 mrxn.guest systemd[1]: Starting LSB: start and stop MySQL...`  
`Dec 24 11:08:59 mrxn.guest mysqld[2138]: Starting MySQL`  
`Dec 24 11:09:00 mrxn.guest mysqld[2138]: ..`  
`Dec 24 11:09:00 mrxn.guest systemd[1]: Started LSB: start and stop MySQL.`

就OK了！

然后根据这个错误我发现了是有人在疯狂的扫描我的博客。。。醉了。。。但是我也不知道为嘛MySQL就抽风了，估计是死锁后我去重启，然后它就抽风了-\_-|

技术文章订阅

- 标签：
- [#Linux](https://mrxn.net/tag/Linux)
- [#emlog](https://mrxn.net/tag/emlog)
- [#MySQL](https://mrxn.net/tag/MySQL)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
