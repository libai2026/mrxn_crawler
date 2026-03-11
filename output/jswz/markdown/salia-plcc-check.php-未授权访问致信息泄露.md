---
title: "Salia PLCC check.php 未授权访问致信息泄露"
source: https://mrxn.net/jswz/salia-check-unauth-data-leak.html
asset_dir: assets/salia-plcc-check.php-未授权访问致信息泄露
---

# Salia PLCC check.php 未授权访问致信息泄露

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/31 08:20
- 717浏览
- [0评论](#comment)
- 2分钟阅读

深入探索

文件大小转换

授权

网络安全课程

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `check.php` 存在信息泄露漏洞，[未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83 "未授权")攻击者可利用该漏洞获取系统敏感信息。

网络安全

# 影响版本

2.2.0（最新版）

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

深入探索

恶意软件分析工具

防火墙软件

安全研究报告

# 漏洞复现

```
GET /check.php HTTP/1.1
Host: salia.mrxn.net
```

比如硬编码的账户和密码

漏洞预警服务

[![Salia PLCC check.php 未授权访问致信息泄露](images/img-001-7b828d417daf.webp)](https://image.mrxn.net/507d63e95cad4279b33380a45aad1ac9.webp)

版本号

深入探索

VPN服务

物流软件安全

编程语言教程

[![Salia PLCC check.php 未授权访问致信息泄露](images/img-002-d03f083bdb24.webp)](https://image.mrxn.net/dc7bf27c45294e3297f53c58042eace9.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
