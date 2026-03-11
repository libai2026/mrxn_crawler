---
title: "天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞"
source: https://mrxn.net/jswz/trwfe-checkDbAvailalbe-ssrf.html
asset_dir: assets/天锐绿盾审批系统-checkdbavailalbe.do-ssrf漏洞
---

# 天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/6 08:28
- 567浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

恶意软件分析工具

漏洞扫描服务

编码转换工具

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控，旨在保护企业和组织的敏感信息，防止未经授权的访问和泄漏。

漏洞预警服务

该系统的 `checkDbAvailalbe.do` 接口存在服务器端请求伪造（[SSRF](https://mrxn.net/tag/SSRF)）漏洞。此漏洞的产生是由于系统在处理用户提供的URL或相关输入时，未能进行充分的验证和过滤，导致攻击者可以操纵服务器发起任意的HTTP请求。

成功利用此[SSRF](https://mrxn.net/tag/SSRF)漏洞，攻击者可以强制服务器向任意内部或外部地址发送请求。这可能导致攻击者绕过防火墙，访问通常无法从外部网络直接访问的内部系统、服务或敏感数据。此外，攻击者还可以利用该漏洞进行内网端口扫描、资产探测，甚至发现并利用内部系统中存在的其他漏洞，从而进一步扩大攻击范围，窃取敏感信息，或在极端情况下实现远程代码执行，对企业数据安全造成严重威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 安全研究工具

# 漏洞分析

先看`checkDbAvailalbe.do`的实现

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-001-c5edd048067e.webp)](https://image.mrxn.net/8d9d5ab544dd42fc8b226e0cfc395af5.webp)

参数`dbIp`, `dbPort`, `dbName`, `dbAccount`, `dbPwd`被带入`MySQLDbUtil.connectable`中，跟进看下它的实现

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-002-2f25649c5ddb.webp)](https://image.mrxn.net/07641941ef544895a70653306a78fbe4.webp)

非常经典的jdbc链接，但是版本为mysql-connector-java-5.1.49为，已经修复了，不能反序列化利用了。不过可以进行探测内网端口开放情况，如果端口开放，则响应时间比较长，否则响应时间很短。

网络安全

深入探索

文本剥离工具

SQL注入防护

安全认证考试

# 漏洞复现

存在且端口开放

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-003-87b7955bca01.webp)](https://image.mrxn.net/f5ecace4c71645379a4ca168d038e36f.webp)

端口不存在

[![天锐绿盾审批系统 checkDbAvailalbe.do SSRF漏洞](images/img-004-e7668cd3eb59.webp)](https://image.mrxn.net/2f522f0d046c4606a646d6aa5bbe0bdb.webp)

二则响应时间长短不同来判断端口开放情况。

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#SSRF](https://mrxn.net/tag/SSRF)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

安全研究工具
