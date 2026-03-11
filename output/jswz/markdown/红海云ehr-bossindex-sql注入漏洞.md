---
title: "红海云eHR BossIndex SQL注入漏洞"
source: https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html
asset_dir: assets/红海云ehr-bossindex-sql注入漏洞
---

# 红海云eHR BossIndex SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/30 08:15
- 448浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

认证

安全

鉴权

---

# 漏洞简介

红海云eHR系统中的BossIndexController（BossIndex.mc、BossIndex.mob等多个方法）模块存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL查询语句，绕过系统认证，实现对数据库的非法访问，获取敏感信息（如用户凭证、个人数据等），甚至在特定条件下可能导致数据库被完全控制，影响范围包括数据访问权限和系统控制权限。

SQL注入防护

# 影响版本

# fofa语法

> body="/RedseaPlatform/skins/images/favicon.ico"
>
> 代码安全审计

# 漏洞分析

## 未授权路由

深入探索

编码转换工具

安全认证考试

漏洞预警服务

先看下 web.xml 里对于这些.mc、.mb和.mob后缀是如何校验的

漏洞修复方案

最开始的CharacterEncodingFilter基础校验，编码校验，这里没有权限校验

[![红海云eHR BossIndex SQL注入漏洞](images/img-001-ed961be18943.webp)](https://image.mrxn.net/32a0ccc6c44a487ba230a4e64682a829.webp)

接着往下看，进入AuthenticationProcessingFilter过滤器

编程

[![红海云eHR BossIndex SQL注入漏洞](images/img-002-e5f059040959.webp)](https://image.mrxn.net/db7d3a1c731742c1a45e2f521273d8f0.webp)

这里是**权限校验**，**校验.mc后缀**，因此网上看到的poc都没有使用此后缀，因为需要权限校验！

网络安全

接下来进入常见的dispatcherServlet过滤器

[![红海云eHR BossIndex SQL注入漏洞](images/img-003-134695d3e31c.webp)](https://image.mrxn.net/a8be342fbf624ecf8976395a2114fb2e.webp)

如图所示，这里没有权限校验，支持的url后缀列表如

数据管理

```
*.mc
*.mob
*.mb
/messageInteface
/cdata
/fdata
/devicecmd
/getrequest
/getrequest.none
/token
/ectpdata
```

## SQL注入

接下来进入本文的正题 **BossIndexController** ，看下它的实现逻辑

SQL注入防护

[![红海云eHR BossIndex SQL注入漏洞](images/img-004-99d8dcb7fcfd.webp)](https://image.mrxn.net/1e843afaefd6463381ec3f84aa81b46d.webp)

如图所示，支持的路由有`"/BossIndex.mc", "/BossIndex.mob"` 两种，结合之前的权限分析可知，我们可选择`/BossIndex.mob` 达到[未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)此接口的目的。

### getNumOfMembers

再看需要的参数`params = {"method=getNumOfMembers"}` 对应的 **getNumOfMembers** 方法里

`String tree_code = req.getParameter("struTreeCode");` 参数`struTreeCode` ==> `tree_code` 然后 `tree_code` 被直接拼接进 `sql1` 和 `sql12` sql语句后，无任何过滤或校验处理直接执行拼接后的SQL语句，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。其他几个方法亦如此，存在同样的sql注入漏洞，下面简单记录下它们的实现。

代码安全审计

### getNewStaffJoin

[![红海云eHR BossIndex SQL注入漏洞](images/img-005-c103cfcb6141.webp)](https://image.mrxn.net/7c23c20874b94f8b8298a323a0584262.webp)

### getNewStaffLeave

[![红海云eHR BossIndex SQL注入漏洞](images/img-006-5eab265ce038.webp)](https://image.mrxn.net/b1036afcdb2240a38f8a4b14ca9cf8a2.webp)

### getNewStaffRetire

[![红海云eHR BossIndex SQL注入漏洞](images/img-007-b4f01f0f212e.webp)](https://image.mrxn.net/1df878a7a54d41b68c725a945d2bb0dd.webp)

### getJoinAndLeaveStaff

[![红海云eHR BossIndex SQL注入漏洞](images/img-008-caafd37ffed9.webp)](https://image.mrxn.net/57cd2277e9ce4650bc3d1dc00b071b37.webp)

### getTodayKaoQin

[![红海云eHR BossIndex SQL注入漏洞](images/img-009-da8b8fc9062b.webp)](https://image.mrxn.net/6f1c58bd6c5f4434a669e8c50282ef80.webp)

### getEarlierWorkStaff

[![红海云eHR BossIndex SQL注入漏洞](images/img-010-587511e012c5.webp)](https://image.mrxn.net/93795f05d0c44d86839da685cadb2d6c.webp)

### getAbsenceStaff

[![红海云eHR BossIndex SQL注入漏洞](images/img-011-402967f27e43.webp)](https://image.mrxn.net/e0d0238d3f524c04bff147af3bd3e236.webp)

所有上述这些方法均存在一个或多个参数的直接拼接导致的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /RedseaPlatform/BossIndex.mob HTTP/1.1
Host: redseaplatform.mrxn.net
Content-Type: application/x-www-form-urlencoded

method=getNumOfMembers&struTreeCode=SQLI_POC
```

[![红海云eHR BossIndex SQL注入漏洞](images/img-012-c77ef558d000.webp)](https://image.mrxn.net/71b1dd0da7734645a16d2c0e061fb371.webp)

成功延 6 秒（执行三次）

编程

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
- [4.1.未授权路由](#toc-4-1-)
- [4.2.SQL注入](#toc-4-2-)
- [4.2.1.getNumOfMembers](#toc-4-2-1-)
- [4.2.2.getNewStaffJoin](#toc-4-2-2-)
- [4.2.3.getNewStaffLeave](#toc-4-2-3-)
- [4.2.4.getNewStaffRetire](#toc-4-2-4-)
- [4.2.5.getJoinAndLeaveStaff](#toc-4-2-5-)
- [4.2.6.getTodayKaoQin](#toc-4-2-6-)
- [4.2.7.getEarlierWorkStaff](#toc-4-2-7-)
- [4.2.8.getAbsenceStaff](#toc-4-2-8-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
