---
title: "金和OA OrderInfoView.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OrderInfoView-sqli.html
asset_dir: assets/金和oa-orderinfoview.aspx-sql注入漏洞
---

# 金和OA OrderInfoView.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/6 13:31
- 272浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

SQL

Windows安全工具

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OrderInfoView.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OrderInfoView.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CrmOrder.dll` 将其进行反编译后找到 **OrderInfoView** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Bind();
  if (this.Request["DataID"] != null)
    this.strOrderID = this.Request["DataID"].ToString();
  this.PageInit();
  this.BindOrderData(this.strOrderID);
}
```

深入探索

JSON处理工具

网络安全培训

漏洞扫描器

跟进`BindOrderData`方法

```
private void BindOrderData(string OrderID)
{
  DataSet dataSet = this.CrmOrd.ReadOrderData(OrderID);
```

跟进`ReadOrderData`方法

[![金和OA OrderInfoView.aspx SQL注入漏洞](images/img-001-5d57916b5a5c.webp)](https://image.mrxn.net/cf4f2a71c4c34432b9397ff81efa73a5.webp)

参数`DataID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CrmOrder/OrderInfoView.aspx/?DataID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OrderInfoView.aspx SQL注入漏洞](images/img-002-e9617f698e23.webp)](https://image.mrxn.net/ac761d07de574aaf8c3fe009b984d743.webp)

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
