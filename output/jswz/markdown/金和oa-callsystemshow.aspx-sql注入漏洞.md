---
title: "金和OA CallSystemShow.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CallSystemShow-sqli.html
asset_dir: assets/金和oa-callsystemshow.aspx-sql注入漏洞
---

# 金和OA CallSystemShow.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/12 08:23
- 624浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

Web安全课程

SQL注入防护

编码转换工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CallSystemShow.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 CallSystemShow.aspx 的源码

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitText();
  if (!this.IsPostBack)
    this.labTime.Text = this.strPublishTime;
  this.LabelMessage.Text = $"<B style=\"COLOR:#ffffff\">{this.strSystemMsg}</B>";
  string MessageID = this.Request["MessageID"].ToString();
  ((Control) this).Page.RegisterHiddenField("MessageID", MessageID);
  DataTable messageInfo = JHBase.Menu.Message.GetMessageInfo(MessageID);
  if (((InternalDataCollectionBase) messageInfo.Rows).Count > 0)
```

在 `bin` 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `CallSystemShow` 的处理逻辑

代码安全审计

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitText();
  if (!this.IsPostBack)
    this.labTime.Text = this.strPublishTime;
  this.LabelMessage.Text = $"<B style=\"COLOR:#ffffff\">{this.strSystemMsg}</B>";
  string MessageID = this.Request["MessageID"].ToString();
  ((Control) this).Page.RegisterHiddenField("MessageID", MessageID);
  DataTable messageInfo = JHBase.Menu.Message.GetMessageInfo(MessageID);
  if (((InternalDataCollectionBase) messageInfo.Rows).Count > 0)
```

深入探索

Web安全书籍

防火墙软件

网络安全会议

跟进 `GetMessageInfo` 方法

```
public static DataTable GetMessageInfo(string MessageID)
{
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable($"select callID,callType,callContent,callTime from callnosee where callID='{MessageID}'");
}
```

参数 `MessageID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /c6/JHBase.Web.Menu/CallSystemShow.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

MessageID='SQLI_POC
```

深入探索

安全运维咨询

Nessus

恶意软件分析工具

[![金和OA CallSystemShow.aspx SQL注入漏洞](images/img-001-86c199b99e1b.webp)](https://image.mrxn.net/8c04cb3b1d67499581b9c4fbb8f2226c.webp)

成功延时 5 秒

漏洞预警服务

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
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
