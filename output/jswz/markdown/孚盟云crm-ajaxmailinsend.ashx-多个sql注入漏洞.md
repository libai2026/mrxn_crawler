---
title: "孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailInSend-sqli.html
asset_dir: assets/孚盟云crm-ajaxmailinsend.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/19 08:31
- 373浏览
- [4评论](#comment)
- 16分钟阅读

深入探索

在线安全工具

技术文章订阅

安全认证考试

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxMailInSend.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxMailInSend.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxMailInSend** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  new SqlAndHtmlChecker(context.Request, context.Response).Check();
  Helper.WriteLog("内分发开始begin", "mailinsend");
  context.Response.ContentType = "text/plain";
  string str1 = UserCookie.GetCookieValue("empId");
  if (!string.IsNullOrEmpty(str1))
    str1 = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(str1);
  string str2 = context.Request["action"];
  if (!string.op_Equality(str2, "autoMailTranRuler"))
  {
    if (!string.op_Equality(str2, "getEmpAndImg"))
      return;
    this.getEmpAndImg(context, str1);
  }
  else
    this.NoAutoMailTranRuler(context.Request["fid"], context.Request["mid"], context.Request["emp"], Convert.ToBoolean(context.Request["auotTrans"]), Convert.ToBoolean(context.Request["transFlag"]), Convert.ToBoolean(context.Request["noticeFlag"]), context.Request["memo"], str1, context);
}
```

深入探索

授权

漏洞预警服务

Windows安全工具

当**action=autoMailTranRuler**时，看下`NoAutoMailTranRuler`方法的实现

代码安全审计

[![孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](images/img-001-c4053572e05f.webp)](https://image.mrxn.net/381d6a00b09743caac2b90bd89d91fc8.webp)

参数**emp**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成SQL注入漏洞。

当**action=getEmpAndImg**时，一样的存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞

[![孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](images/img-002-bdb839b06ff2.webp)](https://image.mrxn.net/ed00e642944943b18ad2026ec08723f6.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxMailInSend.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=autoMailTranRuler&emp=1)SQLI_POC&fid=&mid=&auotTrans=false&transFlag=false&noticeFlag=false&memo=
```

[![孚盟云CRM AjaxMailInSend.ashx 多个SQL注入漏洞](images/img-003-0a86f41677b1.webp)](https://image.mrxn.net/65850bbda50849efb4466e5020b369e8.webp)

成功通过报错注入在响应回显数数据库用户信息

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

网络安全
