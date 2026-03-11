---
title: "Linux - Mrxn's Blog - 专注Web安全"
source: https://mrxn.net/jswz/Linux
asset_dir: assets/linux-mrxn's-blog-专注web安全
---

深入探索

操作系统

LInux

linux

脚本

kali Linux

Linux

kali

代理服务器

UNIX

软件


(adsbygoogle = window.adsbygoogle || []).push({});

* [![OpenWrt passwall 定时自动切换节点](images/img-001-9b56b2e44b5a.webp)](https://mrxn.net/Linux/how-to-auto-change-openwrt-passwall-default-nodes-with-crontab.html)

  + 2025/3/1
  + [Linux](https://mrxn.net/jswz/Linux)

  [OpenWrt passwall 定时自动切换节点](https://mrxn.net/Linux/how-to-auto-change-openwrt-passwall-default-nodes-with-crontab.html)

  前言
  在使用 OpenWrt 的 passwall 插件时，有时你需要在特定的时间切换到特定节点，除了去后台手动切换，其实还可以在后台通过 uci 命令自动切换节点。
  uci 是什么？
  UCI（Unified Configuration Interface）...

  + 2603阅读
  + [0评论](https://mrxn.net/Linux/how-to-auto-change-openwrt-passwall-default-nodes-with-crontab.html#comment)
* [![nmap 错误 Couldn't open a raw socket. Error: Permission denied (13)](images/img-002-6d8696d8199d.png)](https://mrxn.net/Linux/710.html)

  + 2023/5/28
  + [Linux](https://mrxn.net/jswz/Linux)

  [nmap 错误 Couldn't open a raw socket. Error: Permission denied (13)](https://mrxn.net/Linux/710.html)

  Nmap简介
  给不知道的朋友做个简述
  Nmap（Network Mapper）是一个网络扫描器和主机检测工...

  + 7901阅读
  + [0评论](https://mrxn.net/Linux/710.html#comment)

深入探索

Windows安全工具

Web安全书籍

技术文章订阅

服务器安全服务

Web安全课程

SQL注入检测工具

授权

安全研究工具

网络安全培训

网页浏览器

* [![使用Linux命令查找占用磁盘空间最大的20个文件](images/img-003-6d8696d8199d.png)](https://mrxn.net/Linux/708.html)

  + 2023/4/15
  + [Linux](https://mrxn.net/jswz/Linux)

  [使用Linux命令查找占用磁盘空间最大的20个文件](https://mrxn.net/Linux/708.html)

  在 Linux 系统中，经常需要查找占用磁盘空间最大的文件，以便及时清理磁盘空间。本文介绍如何使用 Linux 命令查找占用磁盘空间最大的文件。
  命令如下：
  find / -type f -not -path "\*/\.\*" -not -path "/pro...

  + 6669阅读
  + [2评论](https://mrxn.net/Linux/708.html#comment)
* [![删除history中指定某条记录](images/img-004-6d8696d8199d.png)](https://mrxn.net/Linux/703.html)

  + 2022/11/30
  + [Linux](https://mrxn.net/jswz/Linux)

  [删除history中指定某条记录](https://mrxn.net/Linux/703.html)

  前言
  目前主流 unix 操作系统中默认的 shell 为 bash，其次就是大家自己安装的 zsh。如果需要删除或清理所有的 history 命令对于常用这类系统的朋友来说并不陌生，那就是 history -cw 即可清除所有的历史操作命令。
  这个命令对于二...

  + 15651阅读
  + [0评论](https://mrxn.net/Linux/703.html#comment)

深入探索

身份验证

Docker加速服务

数据库

编码转换工具

漏洞修复方案

网络安全课程

VPN服务

操作系统

Linux

kali Linux

* [![一行命令Linux 统计长连接的外部 IP 地址](images/img-005-aa724e5cc05a.gif)](https://mrxn.net/Linux/691.html)

  + 2022/3/22
  + [Linux](https://mrxn.net/jswz/Linux)

  [一行命令Linux 统计长连接的外部 IP 地址](https://mrxn.net/Linux/691.html)

  命令如下：
  netstat -na|grep ESTABLISHED|awk {'print $5'}|awk -F ':' {'print $1'}|grep -v '127.0.0.1'|sort|uniq -c|sort -rn|head -n 10
  ...

  + 6435阅读
  + [0评论](https://mrxn.net/Linux/691.html#comment)
* [![一行命令快速筛选出高可靠的代理](images/img-006-aa724e5cc05a.gif)](https://mrxn.net/Linux/690.html)

  + 2022/3/18
  + [Linux](https://mrxn.net/jswz/Linux)

  [一行命令快速筛选出高可靠的代理](https://mrxn.net/Linux/690.html)

  前言
  前段时间在 github 上从 pry0cc/soxy 改造过的 check\_proxy 一个由 golang 开发的命令行验证 socks 代理有效性工具。
  这个工具是为命令行使用而生，故只支持从 stdin 输入数据，我们可以通过cat 或者 pb...

  + 6176阅读
  + [0评论](https://mrxn.net/Linux/690.html#comment)

深入探索

云安全解决方案

代码安全审计

JSON处理工具

SQL注入防护

计算机安全

企业安全咨询

安全研究报告

linux

Kali Linux

软件

* [![linux 一行命令获取开机时间](images/img-007-aa724e5cc05a.gif)](https://mrxn.net/Linux/688.html)

  + 2022/3/8
  + [Linux](https://mrxn.net/jswz/Linux)

  [linux 一行命令获取开机时间](https://mrxn.net/Linux/688.html)

  一行命令获取开机时间
  命令：
  w|awk 'NR==1'|awk -F ' ' '{ print $2" "$3$4$5 }'|awk '{ gsub(/\\,/," "); print $0 }'
  效果如下：
  ~/Downloads> w|awk '...

  + 6072阅读
  + [1评论](https://mrxn.net/Linux/688.html#comment)
* [![update-golang：一个帮助你快速安装或者更新到最新版 golang 的 Linux 脚本](images/img-008-aa724e5cc05a.gif)](https://mrxn.net/Linux/595.html)

  + 2021/9/29
  + [Linux](https://mrxn.net/jswz/Linux)

  [update-golang：一个帮助你快速安装或者更新到最新版 golang 的 Linux 脚本](https://mrxn.net/Linux/595.html)

  前言：
  自己的服务器，或者是朋友的服务器，每次想编译 golang 的程序的时候，总是按照既定的步骤去官网下载-解压-安装-添加到环境变量里面，重复的劳动还是恼火。遂想自己写个安装脚本，但是在浏览 github 的时候，发现已经有人写好了的...

  + 6006阅读
  + [0评论](https://mrxn.net/Linux/595.html#comment)

深入探索

unix

nmap

Kali

代理

Linux 系统

安装

脚本语言

Network Mapper

Nmap

Kali Linux

* [![Debian10 x64 build make install Haproxy v2.2.0-在Debian10 64位系统编译安装最新版 Haproxy v2.2.0版本](images/img-009-aa724e5cc05a.gif)](https://mrxn.net/Linux/668.html)

  + 2020/7/16
  + [Linux](https://mrxn.net/jswz/Linux)

  [Debian10 x64 build make install Haproxy v2.2.0-在Debian10 64位系统编译安装最新版 Haproxy v2.2.0版本](https://mrxn.net/Linux/668.html)

  haproxy是一个由C语言编写主要应用于高可用性和负载均衡的应用层代理软件。
   
  今天需要用到haproxy，但是无奈通过系统 Debian10 自带的软件源安装的版本太低了 apt install -y haproxy ；故自行前往官网：http...

  + 3182阅读
  + [0评论](https://mrxn.net/Linux/668.html#comment)
* [![宝塔(bt.cn)面板开启域名登录并且使用域名证书,解决浏览器信任证书问题](images/img-010-aa724e5cc05a.gif)](https://mrxn.net/Linux/Onekey-Open-BT-panel-ssl-with-domain.html)

  + 2018/8/22
  + [Linux](https://mrxn.net/jswz/Linux)

  [宝塔(bt.cn)面板开启域名登录并且使用域名证书,解决浏览器信任证书问题](https://mrxn.net/Linux/Onekey-Open-BT-panel-ssl-with-domain.html)

  PS：最近因为工作原因，很忙，没时间写博客，各位读者，当你们每次打开都没有更新的时候，给你们说一声抱歉。
  Onekey-Open-BT-panel-ssl-with-domain
  宝塔(bt.cn)面板开启域名登录并且使用域名证书,解决浏览器信任证书问题,强迫...

  + 5605阅读
  + [20评论](https://mrxn.net/Linux/Onekey-Open-BT-panel-ssl-with-domain.html#comment)
* [![一键搭建kms激活服务端&&Windows客户端一键激活脚本](images/img-011-aa724e5cc05a.gif)](https://mrxn.net/Linux/kms-server-deploy.html)

  + 2018/4/7
  + [Linux](https://mrxn.net/jswz/Linux)

  [一键搭建kms激活服务端&&Windows客户端一键激活脚本](https://mrxn.net/Linux/kms-server-deploy.html)

  update:06/10/2019 ：
  脚本加入开机自启动，完善逻辑，添加两种零售版转vol版本工具。shell是从vlmcsd仓库拉取编译，你安装的时候就是最新的，不要再问了。
  shell在centos6/7 ubuntu 16 测试没问题，有问...

  + 38121阅读
  + [66评论](https://mrxn.net/Linux/kms-server-deploy.html#comment)
* [![windows10安装kali子系统&&https: aptMethod::Configuration: could not load seccomp policy: Invalid argument解决办法](images/img-012-aa724e5cc05a.gif)](https://mrxn.net/Linux/windows10-install-wsl-kali.html)

  + 2018/3/19
  + [Linux](https://mrxn.net/jswz/Linux)

  [windows10安装kali子系统&&https: aptMethod::Configuration: could not load seccomp policy: Invalid argument解决办法](https://mrxn.net/Linux/windows10-install-wsl-kali.html)

  windwos10安装kali Linux子系统，后更新系统若是出现如下错误：
  https: aptMethod::Configuration: could not load seccomp policy: Invalid argument
  一般是你的源有问...

  + 11431阅读
  + [18评论](https://mrxn.net/Linux/windows10-install-wsl-kali.html#comment)
* [![linux 文件权限字符表示&数字表示](images/img-013-aa724e5cc05a.gif)](https://mrxn.net/Linux/online-linux-chmod-permissions.html)

  + 2018/3/18
  + [Linux](https://mrxn.net/jswz/Linux)

  [linux 文件权限字符表示&数字表示](https://mrxn.net/Linux/online-linux-chmod-permissions.html)

  在线地址：https://mrxn.net/linux-chmod-permissions.html

  + 3009阅读
  + [4评论](https://mrxn.net/Linux/online-linux-chmod-permissions.html#comment)
* [![系统中X1-lock进程Xorg占用CPU爆表通过shell脚本解决以及shell一些知识【笔记】](images/img-014-aa724e5cc05a.gif)](https://mrxn.net/Linux/kill-x1-lock-xorg-with-shell.html)

  + 2018/3/4
  + [Linux](https://mrxn.net/jswz/Linux)

  [系统中X1-lock进程Xorg占用CPU爆表通过shell脚本解决以及shell一些知识【笔记】](https://mrxn.net/Linux/kill-x1-lock-xorg-with-shell.html)

  首先看一下这张CPU的近一周的波动统计图，可以知道从2月28日开始一路飙升，并且后来时不时的自动停止，这个起伏真的是 因吹丝挺啊!(小声嘀咕:QNMLGB！
  我那两天忙，没时间看，这几天空了上去一看傻眼了。。。CPU爆表啊，.X1-lock占用CPU98% ...

  + 8517阅读
  + [0评论](https://mrxn.net/Linux/kill-x1-lock-xorg-with-shell.html#comment)
* [![Kali一键安装docker脚本](images/img-015-aa724e5cc05a.gif)](https://mrxn.net/Linux/install_docker_script_for_Kali.html)

  + 2017/10/29
  + [Linux](https://mrxn.net/jswz/Linux)

  [Kali一键安装docker脚本](https://mrxn.net/Linux/install_docker_script_for_Kali.html)

  Kali不介绍,docker简单的介绍一下:如何通俗解释docker是什么 我的理解用一句话来说就是:在你的系统里面装一个盒子,盒子里你可以干任何事!另外,在gitbook上也有专门的专题介绍,想详细的了解的可以去看一下:
  https://yeasy...

  + 6085阅读
  + [0评论](https://mrxn.net/Linux/install_docker_script_for_Kali.html#comment)
* [![linux下解压rar格式的文件](images/img-016-aa724e5cc05a.gif)](https://mrxn.net/Linux/linux-rar.html)

  + 2017/10/21
  + [Linux](https://mrxn.net/jswz/Linux)

  [linux下解压rar格式的文件](https://mrxn.net/Linux/linux-rar.html)

  linux下一般都是tar和zip的,如果下载到的文件是rar格式的话.我们就需要另外安装rar解压缩软件来支持了.下面简记一下
  首先从rarlab官网的下载页面找到你所对应的版本.32位或者是64位的linux版本.
  https://www.rarlab.c...

  + 4018阅读
  + [0评论](https://mrxn.net/Linux/linux-rar.html#comment)
* [![Linux 下十大命令行下载工具(转)](images/img-017-aa724e5cc05a.gif)](https://mrxn.net/Linux/top-10-command-line-tools-downloading-linux.html)

  + 2017/10/21
  + [Linux](https://mrxn.net/jswz/Linux)

  [Linux 下十大命令行下载工具(转)](https://mrxn.net/Linux/top-10-command-line-tools-downloading-linux.html)

  我们一想到Linux，肯定会想到黑白终端，真正的Linux用户总是偏爱从终端来进行工作，哪怕是用于下载。相比某种GUI工具，命令行下载工具可以帮助用户更迅速地从网上下载任何东西。有许多可满足一般用途、甚至用于torrent的下载工具，不过相比其它工具，只有像c...

  + 2534阅读
  + [0评论](https://mrxn.net/Linux/top-10-command-line-tools-downloading-linux.html#comment)
* [![linux使用问题处理小计(勿入)](images/img-018-aa724e5cc05a.gif)](https://mrxn.net/Linux/578.html)

  + 2017/10/5
  + [Linux](https://mrxn.net/jswz/Linux)

  [linux使用问题处理小计(勿入)](https://mrxn.net/Linux/578.html)

  在ubuntu10.10下没有dig命令，而debian6下面有这个命令ubuntu下想要apt-get安装，发现没有找到dig软件包搜索后才发现正确安装是安装dnsutils
  apt-get install dnsutils
  PS:redhat系列这样安...

  + 3244阅读
  + [2评论](https://mrxn.net/Linux/578.html#comment)
* [![为nginx添加这些额外的第三方扩展加速你的web吧](images/img-019-aa724e5cc05a.gif)](https://mrxn.net/Linux/nginx_add_module.html)

  + 2017/10/1
  + [Linux](https://mrxn.net/jswz/Linux)

  [为nginx添加这些额外的第三方扩展加速你的web吧](https://mrxn.net/Linux/nginx_add_module.html)

  Nginx 是一款高性能 Web 服务器软件，其有非常有益的IO表现，而且相较于 Apache Httpd 配置更加简单上手更加容易，本文将向大家介绍编译安装 Nginx 的第三方扩展。
  Nginx 的额外扩展：
  OpenSSL 1.1...

  + 4073阅读
  + [4评论](https://mrxn.net/Linux/nginx_add_module.html#comment)
* [![两种方式反代Google(镜像)--nginx反代和nginx扩展](images/img-020-aa724e5cc05a.gif)](https://mrxn.net/Linux/nginx_http_google_filter.html)

  + 2017/9/24
  + [Linux](https://mrxn.net/jswz/Linux)

  [两种方式反代Google(镜像)--nginx反代和nginx扩展](https://mrxn.net/Linux/nginx_http_google_filter.html)

  写这篇文章的缘由是看见了我的博友Secret他写了一篇文章:
  造轮子之谷歌镜像站 让我想起了 之前自己折腾过的nginx扩展镜像Google,效率比这个高,而且支持高级的配置,多级配合组成类似集群的功能,今天又折腾了一下,所以写一下过程,以...

  + 5667阅读
  + [4评论](https://mrxn.net/Linux/nginx_http_google_filter.html#comment)
* [![利用grep,cut,awk处理一些文本的简记](images/img-021-aa724e5cc05a.gif)](https://mrxn.net/Linux/549.html)

  + 2017/3/30
  + [Linux](https://mrxn.net/jswz/Linux)

  [利用grep,cut,awk处理一些文本的简记](https://mrxn.net/Linux/549.html)

  先来案例一波:
  grep (global search regular expression(RE) and print out the line,全面搜索正则表达式并把行打印出来)是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并...

  + 3692阅读
  + [0评论](https://mrxn.net/Linux/549.html#comment)
* [![centos开启ssh密钥登录总结](images/img-022-aa724e5cc05a.gif)](https://mrxn.net/Linux/547.html)

  + 2017/3/29
  + [Linux](https://mrxn.net/jswz/Linux)

  [centos开启ssh密钥登录总结](https://mrxn.net/Linux/547.html)

  centos开启SSH的密钥登录相信大家都会吧,而且很多的一键脚本都会配备,比如wdlinux面板的一件安装包都会配备而且支持自定义修改SSH端口,和一键生成密钥,很方便的,但是我们有时候没有必要安装这些一键脚本(比如内存小,不是用来做web服务的...

  + 3517阅读
  + [0评论](https://mrxn.net/Linux/547.html#comment)
* [![LInux远程文件传输效率工具-lrzsz](images/img-023-aa724e5cc05a.gif)](https://mrxn.net/Linux/542.html)

  + 2017/3/20
  + [Linux](https://mrxn.net/jswz/Linux)

  [LInux远程文件传输效率工具-lrzsz](https://mrxn.net/Linux/542.html)

  相信作为linux运维的童鞋们都会遇到这么一个问题，那就是当你使用xshell或者SecureCRT，你会发现，想在自己本地和服务器进行文件传输是一件很麻烦的事情，当然，你会说可以使用ftp可以用sftp，但是这些方式太麻烦了，我也经常为这些问题困扰...

  + 2856阅读
  + [4评论](https://mrxn.net/Linux/542.html#comment)
* [![error while loading shared libraries: libsodium.so.18: cannot open shared](images/img-024-aa724e5cc05a.gif)](https://mrxn.net/Linux/541.html)

  + 2017/3/20
  + [Linux](https://mrxn.net/jswz/Linux)

  [error while loading shared libraries: libsodium.so.18: cannot open shared](https://mrxn.net/Linux/541.html)

  昨晚在部署环境编译pureFTP的时候,报错:
  error while loading shared libraries: libsodium.so.18: cannot open...

  + 6473阅读
  + [0评论](https://mrxn.net/Linux/541.html#comment)
* [![Linux Find 命令精通指南(转)](images/img-025-aa724e5cc05a.gif)](https://mrxn.net/Linux/539.html)

  + 2017/3/17
  + [Linux](https://mrxn.net/jswz/Linux)

  [Linux Find 命令精通指南(转)](https://mrxn.net/Linux/539.html)

  简单介绍这一无处不在的命令的强大的方面以及混乱的方面。
  2008 年 7 月发布
  Linux find 命令是所有 Linux 命令中最有用的一个，同时也是最混乱的一个。它很难，因为它的语法与其他 Linu...

  + 2184阅读
  + [0评论](https://mrxn.net/Linux/539.html#comment)
* [![搭建 nginx + mysql + php-fpm 环境（CentOS 6）](images/img-026-aa724e5cc05a.gif)](https://mrxn.net/Linux/536.html)

  + 2017/3/6
  + [Linux](https://mrxn.net/jswz/Linux)

  [搭建 nginx + mysql + php-fpm 环境（CentOS 6）](https://mrxn.net/Linux/536.html)

  前言:这几天帮朋友部署一个项目,一开始为了方便,(我懒-\_-|),使用一键lanmp脚本部署,结果项目测试的时候bug一大堆...,声明:这不是说这些一键脚本不好,客观的来说,这些脚本用来建站,普通的单纯的站,一般没问题的,也很方便,但是部署项目,如...

  + 2376阅读
  + [0评论](https://mrxn.net/Linux/536.html#comment)
* [![在UEFI+GPT下使用rEFind实现Win10 + Kali2.0 双引导](images/img-027-aa724e5cc05a.gif)](https://mrxn.net/Linux/UEFI-GPT-rEFind-Win10-Kali20.html)

  + 2017/2/2
  + [Linux](https://mrxn.net/jswz/Linux)

  [在UEFI+GPT下使用rEFind实现Win10 + Kali2.0 双引导](https://mrxn.net/Linux/UEFI-GPT-rEFind-Win10-Kali20.html)

  前言:转载这篇文章主要是因为以下几点原因:
  我的这篇博文主要是在硬盘分区为mbr+bios(更多gpt+mbr介绍点我)启动的情况下安装的Kali.详情:https://mrxn.net/Linux/363.html&n...

  + 6422阅读
  + [8评论](https://mrxn.net/Linux/UEFI-GPT-rEFind-Win10-Kali20.html#comment)
* [![Kali渗透测试演练Metasploitable靶机(附详细word文档+乌云_vmware_201606)](images/img-028-aa724e5cc05a.gif)](https://mrxn.net/Linux/Use-Kali-Metasploitable-do-sth-test.html)

  + 2017/1/28
  + [Linux](https://mrxn.net/jswz/Linux)

  [Kali渗透测试演练Metasploitable靶机(附详细word文档+乌云\_vmware\_201606)](https://mrxn.net/Linux/Use-Kali-Metasploitable-do-sth-test.html)

  Kali渗透测试演练Metasploitable靶机
  准备工作：
  l VM虚拟机（http://www.vmware.com/cn.html）
  l Kali（https://www.off...

  + 5269阅读
  + [2评论](https://mrxn.net/Linux/Use-Kali-Metasploitable-do-sth-test.html#comment)
* [![利用 iptables 折腾安全的服务器环境](images/img-029-aa724e5cc05a.gif)](https://mrxn.net/Linux/iptables-use-note.html)

  + 2016/4/2
  + [Linux](https://mrxn.net/jswz/Linux)

  [利用 iptables 折腾安全的服务器环境](https://mrxn.net/Linux/iptables-use-note.html)

  0x00 概述
  iptables 是 Linux 内核集成一套包过滤系统，并且可以实现状态防火墙，建立精细的包过滤列表，功能十分强大，所以选择折腾 iptables 来实现防火墙。
  iptables 一共有 4 个表：filt...

  + 9243阅读
  + [0评论](https://mrxn.net/Linux/iptables-use-note.html#comment)
* [![linux执行shell脚本的方式及一些区别](images/img-030-aa724e5cc05a.gif)](https://mrxn.net/Linux/different-linux-shell-do.html)

  + 2016/3/28
  + [Linux](https://mrxn.net/jswz/Linux)

  [linux执行shell脚本的方式及一些区别](https://mrxn.net/Linux/different-linux-shell-do.html)

  假设shell脚本文件为hello.sh
  放在/root目录下。下面介绍几种在终端执行shell脚本的方法：
  [root@localhost home]# cd /root/
  [root@localhost ~]#vim ...

  + 4847阅读
  + [0评论](https://mrxn.net/Linux/different-linux-shell-do.html#comment)

1 [2](https://mrxn.net/jswz/Linux/page/2)

(adsbygoogle = window.adsbygoogle || []).push({});