---
title: "Oracle 11g sys和system用户密码都忘记了的解决办法"
source: https://mrxn.net/jswz/modified-Oracle-system-password.html
asset_dir: embedded-base64
---

最近因为工作需要在学习Oracle，但是我这个人记性不好，当初设置的system密码忘了。

[搜索](#)查看了很多的关于忘记Oracle密码的解决办法，加上自己的亲自实践（前车之鉴），得出如下方法修改你忘记的Oracle中的system这些用户密码，很简单，只有几步。

第一步，打开的sqlplus.(系统菜单Oracle下面的或者是cmd里面你输入sqlplus都可以)

数据管理

第二步，在弹出的输入用户名界面输入 /as sysdba 然后使劲儿啪的一下敲下你的回车键！

SQL\*Plus: Release 11.2.0.1.0 Production on 星期四 4月 26 14:09:47 2018

Copyright (c) 1982, 2010, Oracle. All rights reserved.

请输入用户名: /as sysdba

连接到:  
Oracle [Database](#) 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production  
With the Partitioning, OLAP, Data Mining and Real Application Testing options

第三步，在SQL>的右边输入：conn sys/sys as sysdba;（我也不知道原理，为嘛这里可以连接）

PS：因为sys的也忘了=\_=|，所以不信的可以去sqlplus下测试应该是如下结果：

请输入用户名: sys  
输入口令:  
ERROR:  
ORA-01017: invalid username/password; logon denied

最后一步，直接使用alter命令修改你要修改的用户密码即可（下面语法中的红色部分1是需要修改的用户名，红色部分2是改成你的新密码）。

语法为：alter user **username** identified by **newpassword**;

深入探索

客户关系管理

网络安全咨询

SQL注入防护

SQL> alter user system identified by system;

编程

用户已更改。

SQL> conn system/system  
已连接。  
SQL>

如果你需要修改的账户是锁定的，比如scott用户，那么只需要在最后一步这里使用如下命令解锁即可：

alter user scott account unlock;

溜了，有时间把自己学习Oracle的笔记贴出来（滥竽充数）。下回见！
