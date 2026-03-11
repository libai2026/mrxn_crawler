---
title: "Supervisor重新加载配置&启动新的进程"
source: https://mrxn.net/jswz/Supervisor-reload-restart.html
asset_dir: assets/supervisor重新加载配置&启动新的进程
---

# Supervisor重新加载配置&启动新的进程

[Mrxn](https://mrxn.net/author/1)- 发表于2018/5/28 15:56
- 6229浏览
- [1评论](#comment)
- 20分钟阅读

深入探索

安装程序

进程

UNIX

---

一、添加好配置文件后。一般是在:/etc/supervisor/目录下,当然，我推荐大家在安装supervisor的时候呢，将主配置文件和其他需要守护的应用程序的配置文件分开，以便于管理和区别，这里把我的主配置文集贴出来，仅供参考：

操作系统

`[unix_http_server]  
;file=/tmp/supervisor.sock ; UNIX socket 文件，supervisorctl 会使用  
file=/home/supervisor/supervisor.sock ; (the path to the socket file)  
;chmod=0700 ; socket 文件的 mode，默认是 0700  
;chown=nobody:nogroup ; socket 文件的 owner，格式： uid:gid  
;[inet_http_server] ; HTTP 服务器，提供 web 管理界面  
;port=127.0.0.1:9001 ; Web 管理后台运行的 IP 和端口，如果开放到公网，需要注意安全性  
;username=usersuper ; 登录管理后台的用户名  
;password=yourpasswd.. ; 登录管理后台的密码  
[supervisord]  
;logfile=/tmp/supervisord.log ; 日志文件，默认是 $CWD/supervisord.log  
logfile=/var/log/supervisor/supervisord.log ;日志文件，修改为专门设置的目录  
logfile_maxbytes=50MB ; 日志文件大小，超出会 rotate，默认 50MB  
logfile_backups=10 ; 日志文件保留备份数量默认 10  
loglevel=info ; 日志级别，默认 info，其它: debug,warn,trace  
;pidfile=/tmp/supervisord.pid ; pid 文件  
pidfile=/home/supervisor/supervisord.pid ;  
nodaemon=false ; 是否在前台启动，默认是 false，即以 daemon 的方式启动  
minfds=1024 ; 可以打开的文件描述符的最小值，默认 1024  
minprocs=200 ; 可以打开的进程数的最小值，默认 200  
; the below section must remain in the config file for RPC  
; (supervisorctl/web interface) to work, additional interfaces may be  
; added by defining them in separate rpcinterface: sections  
[rpcinterface:supervisor]  
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface  
[supervisorctl]  
;serverurl=unix:///tmp/supervisor.sock ; 通过 UNIX socket 连接 supervisord，路径与 unix_http_server 部分的 file 一致  
serverurl=unix:///home/supervisor/supervisor.sock ;  
;serverurl=http://127.0.0.1:9001 ; 通过 HTTP 的方式连接 supervisord  
; 包含其他的配置文件  
[include]  
files = /etc/supervisor/*.conf ; 可以是 *.conf 或 *.ini`

深入探索

Web安全书籍

Windows安全工具

漏洞修复方案

二、更新新的配置到supervisord

软件

`supervisorctl update`

三、重新启动配置中的所有程序

`supervisorctl reload`

四、启动某个进程(program\_name=你配置中写的程序名称)

`supervisorctl start program_name`

五、查看正在守候的进程

`supervisorctl`

六、停止某一进程 (program\_name=你配置中写的程序名称)

`pervisorctl stop program_name`

七、重启某一进程 (program\_name=你配置中写的程序名称)

操作系统

`supervisorctl restart program_name`

八、停止全部进程

`supervisorctl stop all`

注意：显示用stop停止掉的进程，用reload或者update都不会自动重启。

- 标签：
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读

网络安全
