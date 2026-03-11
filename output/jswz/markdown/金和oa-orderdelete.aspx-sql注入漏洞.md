---
title: "金和OA OrderDelete.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OrderDelete-sqli.html
asset_dir: assets/金和oa-orderdelete.aspx-sql注入漏洞
---

# 金和OA OrderDelete.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/5 13:31
- 286浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

服务器

软件

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OrderDelete.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OrderDelete.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CrmOrder.dll` 将其进行反编译后找到 **OrderDelete** 的处理逻辑

深入探索

防火墙软件

恶意软件分析工具

编程语言教程

```
protected void Page_Load(object sender, EventArgs e)
{
  this.KeyCtrl("JHICRM");
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Bind();
  if (this.Request["DataID"] != null)
    this.strOrderID = this.Request["DataID"].ToString();
  this.PageInit();
  this.BindOrderData(this.strOrderID);
}
```

跟进`BindOrderData`方法

```
private void BindOrderData(string OrderID)
{
  DataSet dataSet = this.CrmOrd.ReadOrderData(OrderID);
```

跟进`ReadOrderData`方法

[![金和OA OrderDelete.aspx SQL注入漏洞](images/img-001-0346ad749409.webp)](https://image.mrxn.net/0ff3c8ae7aa64362946c1f4606bc6ce1.webp)

参数`DataID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CrmOrder/OrderDelete.aspx/?DataID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OrderDelete.aspx SQL注入漏洞](images/img-002-0a01440ba099.webp)](https://image.mrxn.net/40fe993df1a446daaf21d19faee3ce6b.webp)

[![金和OA OrderDelete.aspx SQL注入漏洞](images/img-003-428d435416e8.webp)](https://image.mrxn.net/e6fd0f88b4d64ebfbbbdecb8501aad27.webp)

成功延时 6 秒

代码安全审计

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
