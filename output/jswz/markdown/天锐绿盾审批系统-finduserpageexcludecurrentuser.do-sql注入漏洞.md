---
title: "天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞"
source: https://mrxn.net/jswz/trwfe-findUserPageExcludeCurrentUser-sqli.html
asset_dir: assets/天锐绿盾审批系统-finduserpageexcludecurrentuser.do-sql注入漏洞
---

# 天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/10 08:30
- 406浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

安全

软件

计算机安全

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控，并常作为OA系统中的加密[软件](#)，实现审批流程的自动化和信息化。

SQL注入防护

天锐绿盾审批系统的 `findUserPageExcludeCurrentUser.do` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可以通过构造恶意的SQL查询参数，直接操控数据库查询语句，从而绕过身份验证，获取未授权的数据、修改数据库内容或执行其他恶意操作。该漏洞可能导致敏感信息泄露，例如用户数据或系统配置信息，严重影响系统的数据完整性和机密性，进而降低整体系统安全性。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 代码安全审计

# 漏洞分析

先看`findUserPageExcludeCurrentUser.do`的实现

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-001-eb7b95748042.webp)](https://image.mrxn.net/b3eca8bc72654510b69371288cfd0bb1.webp)

看下PageVo对象的定义

漏洞修复方案

深入探索

在线安全工具

网络安全会议

传输层安全性协议

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-002-292dea5afb65.webp)](https://image.mrxn.net/378e8c5797ac428fb80b7a5ddd2c0bf2.webp)

在 `getPageSql()` 方法中，来自用户请求的 `sort` 和 `order` 成员变量被直接拼接到 `pageSql` 字符串中。由于这两个变量的值完全由用户控制且未经过任何安全处理，攻击者可以构造恶意的 SQL 片段。

安全运维咨询

再跟进`findDeptUser` 方法，看下`findDeptUser`最终的**MyBatis 映射文件内容**

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-003-28ca18fa7eda.webp)](https://image.mrxn.net/e0c85ea74dcf4a40a52a4ab30b57368c.webp)

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-004-b570664f1541.webp)](https://image.mrxn.net/412f1aae164441d1b3ada9f2760feeb4.webp)

此处的 `${pageVo.pageSql}` 语法在 MyBatis 中表示直接进行字符串替换，而不是使用预编译的参数化查询（`#{...}`）。这意味着 `pageSql` 变量的内容将作为原始SQL代码的一部分被执行，这是导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的直接原因。

物流软件安全

该代码段提供了一个分页查询租户信息（Tenant）的功能。前端通过调用 `/findUserPageExcludeCurrentUser.do` 接口，并传递 `page`、`rows`、`sort`、`order` 等参数来控制分页和排序逻辑。后端接收到参数后，通过 `PageVo` 对象进行封装，并最终调用 MyBatis 执行数据库查询。

由于后端在处理排序参数 `sort` 和 `order` 时，未进行任何安全校验或过滤，直接将这些参数拼接到 SQL 语句中，造成了 **[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞**。攻击者可以利用此漏洞执行任意数据库操作，例如窃取数据、篡改信息，甚至在特定数据库和权限配置下获取服务器控制权。

编程

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/user/findUserPageExcludeCurrentUser.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

deptId=1&sort=a.ID_SQLI_POC
```

成功延时 5 秒

数据管理

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-005-810586842da2.webp)](https://image.mrxn.net/4148fafe01a645ea90db23d75c0c3db6.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
