---
title: "孚盟云CRM AjaxReadMail.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxReadMail-sqli.html
asset_dir: assets/孚盟云crm-ajaxreadmail.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxReadMail.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/26 08:31
- 252浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

SaaS

CRM

application

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxReadMail.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

安全工具开发

技术文章订阅

JSON处理工具

直接看 `AjaxReadMail.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxReadMail** 方法的实现如下

```
string str3 = context.Request["method"].ToString();
string empty8 = string.Empty;
string empty9 = string.Empty;
string s = str3;
switch (\u003CPrivateImplementationDetails\u003E.ComputeStringHash(s))
{
...
if (!string.op_Equality(s, "getHeadImage"))
  break;
try
{
  string empPic = new VTSupport().GetEmpPic(context.Request["empId"] == null ? "" : context.Request["empId"].ToString());
  context.Response.Write(empPic);
  break;
}
```

深入探索

身份验证

app

VPN服务

当**method=GetEmpPic**时，进入`GetEmpPic`方法

```
public string GetEmpPic(string empId)
{
  DataTable table = this.dbHelper.Query($"select * from bfEmp where EmpID='{empId}' ").Tables[0];
  return this.getEmpPicHtml(table.Rows[0]["HeadPic"].ToString(), table.Rows[0]["CNEmpName"].ToString(), empId);
}
```

参数`empID`被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

downLoadAttachFiles方法也存在同样的拼接导致的SQL注入漏洞。

SQL注入防护

[![孚盟云CRM AjaxReadMail.ashx SQL注入漏洞](images/img-001-38e0825910cd.webp)](https://image.mrxn.net/e2f05fd51dd04eef973c217283816d22.webp)

# 漏洞复现

深入探索

安全研究工具

安全认证考试

Web安全书籍

```
POST /m/Dingding/Ajax/AjaxReadMail.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=getHeadImage&empId='SQLI_POC--
```

[![孚盟云CRM AjaxReadMail.ashx SQL注入漏洞](images/img-002-08476d09d510.webp)](https://image.mrxn.net/5983c0df0d5a48f182b14f3c51b59283.webp)

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
