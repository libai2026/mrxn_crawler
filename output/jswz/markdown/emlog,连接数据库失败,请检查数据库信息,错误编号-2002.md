---
title: "emlog,连接数据库失败,请检查数据库信息,错误编号 2002"
source: https://mrxn.net/jswz/emlog-mysql-2002error-solved.html
asset_dir: embedded-base64
---

今天起来发现博客打不开了，提示：连接数据库失败,请检查数据库信息,错误编号 2002。

数据管理

首先看这个错误代码是2002，并不是[emlog](https://mrxn.net/tag/emlog "标签：emlog")的配置文件有问题，因为从include/lib/[MySQL](https://mrxn.net/tag/MySQL "标签：MySQL").php里面可以看到这个2002应该是MySQL本身出问题了，但是不一定，下面来排查是不是MySQL本身出问题了。

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

Web安全博客

网络安全咨询

Windows安全工具

登上服务器，准备登录[MySQL](https://mrxn.net/tag/MySQL "标签：MySQL")，mysql -uroot -ppassword，报错如下：

ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)

编程

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

数据管理

问题原因就这与MySQL本身没有启动起来。我们先停止MySQL试试：service mysqld stop ，然后查看状态：

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

然后Google[搜索](#)上面的红色关键词：Couldn't find MySQL server (/usr/bin/mysqld\_safe) ... failed! ，借鉴这个的方法 <http://www.cnblogs.com/olinux/p/5546371.html>

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

数据管理

然后根据这个错误我发现了是有人在疯狂的扫描我的博客。。。醉了。。。但是我也不知道为嘛MySQL就抽风了，估计是死锁后我去重启，然后它就抽风了-\_-|
