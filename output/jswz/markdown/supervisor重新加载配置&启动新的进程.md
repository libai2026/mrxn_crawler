---
title: "Supervisor重新加载配置&启动新的进程"
source: https://mrxn.net/jswz/Supervisor-reload-restart.html
asset_dir: embedded-base64
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

网站托管与域名注册

编程

客户关系管理

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
