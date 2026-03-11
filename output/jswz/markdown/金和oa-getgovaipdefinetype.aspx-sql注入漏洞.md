---
title: "金和OA getGovAIPDefineType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-getGovAIPDefineType-sqli.html
asset_dir: assets/金和oa-getgovaipdefinetype.aspx-sql注入漏洞
---

# 金和OA getGovAIPDefineType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/15 13:31
- 204浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

漏洞扫描器

JSON处理工具

安全工具开发

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `getGovAIPDefineType.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `getGovAIPDefineType.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.govsetaip.dll` 将其进行反编译后找到 **getGovAIPDefineType** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (((Control) this).Page.IsPostBack)
    return;
  string strType = this.Request["strType"].ToString();
  string strId = this.Request["intId"].ToString();
  if (!string.op_Inequality(strId, ""))
    return;
  DataTable govAipDefineType = new GovType().getGovAIPDefineType(strType, strId);
  if (((InternalDataCollectionBase) govAipDefineType.Rows).Count > 0)
    this.Response.Write(govAipDefineType.Rows[0][0].ToString());
  else
    this.Response.Write("NO");
}
```

深入探索

在线安全工具

Windows安全工具

安全认证考试

跟进`getGovAIPDefineType`方法

```
public DataTable getGovAIPDefineType(string strType, string strId)
{
  string str = $"select sysF_Name from dbo.GovPaperAip where SysFile_Type='{strType}' and Default_Flag='{strId}'";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

参数`strType`、`intId`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govsetaip/getGovAIPDefineType.aspx/?strType=SQLI_POC&intId=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

Web安全课程

文件大小转换

安全

[![金和OA getGovAIPDefineType.aspx SQL注入漏洞](images/img-001-b8ac519e691e.webp)](https://image.mrxn.net/d3502b9b822b4f6c98edd9fdf4a8d9cd.webp)

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
