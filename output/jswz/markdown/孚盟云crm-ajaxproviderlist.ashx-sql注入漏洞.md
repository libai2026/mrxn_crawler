---
title: "孚盟云CRM AjaxProviderList.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxProviderList-sqli.html
asset_dir: assets/孚盟云crm-ajaxproviderlist.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxProviderList.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/25 08:31
- 225浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

CRM

应用程序

客户关系管理

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxProviderList.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxProviderList.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxProviderList** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  if (string.IsNullOrEmpty(UserCookie.GetCookieValue("empId")))
    return;
  this.empId = UserCookie.GetCookieValue("empId");
  this.empId = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(this.empId);
  string str = context.Request["method"].ToString();
  if (!string.op_Equality(str, "more"))
  {
    if (!string.op_Equality(str, "showSate"))
    {
      if (!string.op_Equality(str, "search"))
      {
        if (!string.op_Equality(str, "SendMessage"))
          return;
        this.SendMessage(context, this.empId);
      }
      else
        this.search(context, this.empId);
    }
    else
      this.showSate(context, this.empId);
  }
  else
    this.more(context, this.empId);
}
```

深入探索

Web安全书籍

网络安全会议

Windows安全工具

当**method=SendMessage**时，进入`SendMessage`方法

```
private void SendMessage(HttpContext context, string empID)
{
  string str1 = context.Request["cid"];
  string str2 = context.Request["FID"];
  string str3 = context.Request["agentId"];
  string str4 = context.Request["url"];
  JsonSerializerSettings settings = new JsonSerializerSettings()
  {
    NullValueHandling = NullValueHandling.Ignore
  };
  string str5 = new CreatePageDao().GetDataSource($"select Dingding from bfEMP where EmpID='{empID}'").Rows[0][0].ToString();
```

参数`empID`被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxProviderList.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"'SQLI_POC--","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=SendMessage
```

[![孚盟云CRM AjaxProviderList.ashx SQL注入漏洞](images/img-001-661e8527e239.webp)](https://image.mrxn.net/2fccc5d3e73148698decc4a95b6a1af7.webp)

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
