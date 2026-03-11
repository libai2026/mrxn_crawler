---
title: "金和OA AskAttachment.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AskAttachment-sqli.html
asset_dir: assets/金和oa-askattachment.aspx-sql注入漏洞
---

# 金和OA AskAttachment.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/23 13:31
- 328浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

SQL

木马

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AskAttachment.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AskAttachment.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Ask.dll` 将其进行反编译后找到 **AskAttachment** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Expires = -1;
  string strFileIdList = this.Request["AttachmentIdList"];
  if (!string.IsNullOrEmpty(strFileIdList))
    this.Response.Write(JHSoft.Ask.Ask.GetAttachmentName(strFileIdList));
  this.Response.End();
}
```

参数`AttachmentIdList`被带入`GetAttachmentName`方法

```
public static string GetAttachmentName(string strFileIdList)
{
  string str = string.Empty;
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select FileName from files where FileId in ({strFileIdList})");
  for (int index = 0; index < ((InternalDataCollectionBase) dataTable.Rows).Count; ++index)
    str = $"{str}{dataTable.Rows[index]["FileName"].ToString()},";
  return !string.IsNullOrEmpty(str) ? str.Substring(0, str.Length - 1) : str;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

深入探索

安全工具开发

安全研究工具

云安全解决方案

```
GET /c6/Jhsoft.Web.Ask/AskAttachment.aspx/?AttachmentIdList=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AskAttachment.aspx SQL注入漏洞](images/img-001-c99a9e3d8743.webp)](https://image.mrxn.net/7bec9eb961eb43d58f408023c2b31657.webp)

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
