---
title: "孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxWriteMail-sqli.html
asset_dir: assets/孚盟云crm-ajaxwritemail.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/27 08:31
- 233浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

授权

在线安全工具

数据库

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxWriteMail.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

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

参数**mails**按照分号分割后被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。empId参数是被直接拼接金SQL语句，也是注入点。

代码安全审计

getContactList、saveCategory、GetCustInfo、excetSpLastTrackInfo、SendMail\_send和SendMail方法也存在同样的拼接导致的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

[![孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞](images/img-001-f6acf1da2b15.webp)](https://image.mrxn.net/d8f94e847c234ad585cecdba3ab72ecd.webp)

[![孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞](images/img-002-99a20b4f3c8e.webp)](https://image.mrxn.net/bfd727a4ad0147458f888f247db217b1.webp)

[![孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞](images/img-003-c7ad29d16bb5.webp)](https://image.mrxn.net/8a17d424f89a465e877650ed234e563f.webp)

[![孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞](images/img-004-140ffa88c3dd.webp)](https://image.mrxn.net/e59de1ce60e44bbfb48bf9e05ea9a470.webp)

[![孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞](images/img-005-bc5ee2fdcc4c.webp)](https://image.mrxn.net/285da401b34f4be487730f64245b6948.webp)

[![孚盟云CRM AjaxWriteMail.ashx SQL注入漏洞](images/img-006-d26038da0098.webp)](https://image.mrxn.net/788e30f8462a4952abc43760e209406e.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxWriteMail.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"admin","corpId": "1"}
Content-Type: application/x-www-form-urlencoded

method=updateLastedContactTable&mails=SQLI_POC
```

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
