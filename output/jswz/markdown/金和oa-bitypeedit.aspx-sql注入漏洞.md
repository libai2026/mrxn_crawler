---
title: "金和OA BITypeEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-BITypeEdit-sqli.html
asset_dir: assets/金和oa-bitypeedit.aspx-sql注入漏洞
---

# 金和OA BITypeEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/26 13:30
- 442浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

网络安全培训

数据库

漏洞预警服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `BITypeEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `BITypeEdit.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.BIframe.dll` 将其进行反编译后找到 **BITypeEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.mod = new commonMethod();
  this.type = this.Request.QueryString["type"].ToString();
  if (string.op_Equality(this.type, "edit"))
    this.strTitle = "修改报表类型";
  if (((Control) this).Page.IsPostBack || !string.op_Equality(this.type, "edit"))
    return;
  ((HtmlInputControl) this.txt_Name).Value = this.mod.GetTypeNameByCode(this.Request.QueryString["id"].ToString());
}
```

当`type=edit`时，参数`id`被带入`GetTypeNameByCode`方法

深入探索

授权

安全研究报告

Nessus

```
public string GetTypeNameByCode(string typeCode)
{
  string empty = string.Empty;
  DataTable tableDate = this.GetTableDate($"select typename from BI_ReportType where typecode='{typeCode}'");
  if (tableDate != null && ((InternalDataCollectionBase) tableDate.Rows).Count > 0)
    empty = tableDate.Rows[0][0].ToString();
  return empty;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.BIframe/BITypeEdit.aspx/?type=edit&id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA BITypeEdit.aspx SQL注入漏洞](images/img-001-bbcdc7f421f5.webp)](https://image.mrxn.net/87d7a800743e469e80ce6c0334515f7e.webp)

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
