---
title: "快普M6 WebService/StaffService.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/kuaipu-WebService-StaffService-GetPositionOfStaff-sqli.html
asset_dir: assets/快普m6-webservicestaffservice.asmx-sql注入漏洞
---

# 快普M6 WebService/StaffService.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/1 08:28
- 751浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

Web服务

数据库

WebService

---

# 漏洞简介

快普M6整合管理平台的[WebService](#)/StaffService.asmx接口下多个方法存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，绕过参数过滤机制，实现对数据库的任意查询、修改或删除操作，甚至可能获取系统控制权限。

网络服务

# 影响版本

# fofa语法

> body="Resource/JavaScript/jKPM6.DateTime.js"

# 漏洞分析

根据漏洞通告，看下 WebService/StaffService.asmx 里的cs引用

```
<%@ WebService Language="C#" CodeBehind="StaffService.asmx.cs" Class="KPMIIS.Web.WebService.StaffService" %>
```

ok,根据引用去找到bin目录下的KPMIIS.Web.dll文件，反编译后找到WebService下的StaffService实现

SQL注入检测工具

```
[System.Web.Services.WebService(Namespace = "http://tempuri.org/")]
[ToolboxItem(false)]
[ScriptService]
[WebServiceBinding]
public class StaffService : System.Web.Services.WebService
{
  [WebMethod]
  public string GetPositionOfStaff()
  {
    string str = HttpContext.Current.Request.Form["sid"];
    DataRow row = Gateway.Default.FromCustomSql("select top 1 organization_name,position_id from dbo.COMMON_PositionToStaff p,dbo.COMMON_Organization o \r\n                                    where p.position_id=o.organization_id and staff_id=" + str).ToDataSet().Tables[0].Rows[0];
    return $"{row[0]},{row[1]}";
  }
}
```

深入探索

安全运维咨询

漏洞修复方案

服务器安全服务

参数**sid**，没有经过任何过滤或校验检查就被拼接进SQL语句中进行执行了，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，非常的朴实无华。

代码安全审计

# 漏洞复现

> 因参数使用**HttpContext.Current.Request.Form**获取，使用常规的GET或POST传参即可

```
POST /WebService/StaffService.asmx/GetPositionOfStaff HTTP/1.1
Host: kuaipu.mrxn.net
Content-Type: application/x-www-form-urlencoded

sid=SQLI_POC
```

[![快普M6 WebService/StaffService.asmx SQL注入漏洞](images/img-001-c9781b4b1005.webp)](https://image.mrxn.net/28df3967fff04a4babdc2d4e2c694294.webp)

成功通过报错注入在响应回显数据库默认用户信息

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
