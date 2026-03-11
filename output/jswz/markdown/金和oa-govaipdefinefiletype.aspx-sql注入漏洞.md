---
title: "金和OA GovAIPDefineFileType.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GovAIPDefineFileType-sqli.html
asset_dir: assets/金和oa-govaipdefinefiletype.aspx-sql注入漏洞
---

# 金和OA GovAIPDefineFileType.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/16 13:31
- 224浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

软件

SQL

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GovAIPDefineFileType.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GovAIPDefineFileType.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.govsetaip.dll` 将其进行反编译后找到 **GovAIPDefineFileType** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (((Control) this).Page.IsPostBack)
    return;
  this.initPage();
  string strId = this.Request["intId"].ToString();
  if (!string.op_Inequality(strId, ""))
    return;
  DataTable searchFileType = new GovType().getSearchFileType(strId);
```

跟进`getSearchFileType`方法

```
public DataTable getSearchFileType(string strId)
{
  string str = $"declare @strFileType varchar(50)  select @strFileType=sysFile_Type from govpaperaip where sysF_ID='{strId}'" + " if(@strFileType='IOA_Send')" + " select TypeID,TypeName from sendType where DelFlag=0 " + " if(@strFileType='IOA_Accept')" + " select TypeID,TypeName from AcceptType where DelFlag=0" + " if(@strFileType='IOA_Ask')" + " select TypeID,TypeName from AskType where DelFlag=0";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

参数`intId`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.govsetaip/GovAIPDefineFileType.aspx/?intId=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GovAIPDefineFileType.aspx SQL注入漏洞](images/img-001-7b8b526c7a67.webp)](https://image.mrxn.net/6fac9cd80ceb4620ae65eb64d062763c.webp)

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
