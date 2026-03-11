---
title: "金和OA Add_Collection.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Add_Collection-sqli.html
asset_dir: assets/金和oa-add_collection.aspx-sql注入漏洞
---

# 金和OA Add\_Collection.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/14 13:31
- 231浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

JSON处理工具

Nessus

安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Add_Collection.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

SQL

编码转换工具

防火墙软件

根据 `Add_Collection.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Govset.dll` 将其进行反编译后找到 **Add\_Collection** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.fieldcode = this.Request["fieldcode"] == null ? "" : this.Request.QueryString["fieldcode"];
  if (((Control) this).Page.IsPostBack)
    return;
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select * from tb_hyz_govfieldmore where fieldcode='{this.fieldcode}'");
  if (dataTable == null || ((InternalDataCollectionBase) dataTable.Rows).Count <= 0)
    return;
  ((HtmlInputControl) this.hidden1).Value = dataTable.Rows[0]["fiedlcollection"].ToString();
}
```

参数`fieldcode`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govset/Add_Collection.aspx/?fieldcode=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Add_Collection.aspx SQL注入漏洞](images/img-001-bbd6d77beab9.webp)](https://image.mrxn.net/b115108be27d41f28f78b5aeabffdafa.webp)

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
