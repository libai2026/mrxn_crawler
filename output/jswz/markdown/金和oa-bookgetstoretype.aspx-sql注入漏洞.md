---
title: "金和OA BookGetStoreType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BookGetStoreType-sqli.html
asset_dir: assets/金和oa-bookgetstoretype.aspx-sql注入漏洞
---

# 金和OA BookGetStoreType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/1 13:30
- 334浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

SQL注入检测工具

漏洞预警服务

计算机安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BookGetStoreType.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BookGetStoreType.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Books.dll` 将其进行反编译后找到 **BookGetStoreType** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  string str = this.Request["StoreID"].ToString();
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select bookTypeID,bookTypeName,bookTypeNumber from booksType where booktypeDelFlag=0 and bookstoreID='{str}' order by booktypenumber");
```

至此，就非常明了了，参数**StoreID**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

深入探索

物流软件安全

安全

网络安全课程

```
GET /c6/Jhsoft.Web.Books/BookGetStoreType.aspx/?StoreID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BookGetStoreType.aspx SQL注入漏洞](images/img-001-165874f57f1d.webp)](https://image.mrxn.net/10f31b20f2dd491d9e6ddaa458f00da8.webp)

成功延时 4 秒

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
