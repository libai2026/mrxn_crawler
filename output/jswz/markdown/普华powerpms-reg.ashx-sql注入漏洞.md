---
title: "普华Powerpms Reg.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-Reg-sqli.html
asset_dir: assets/普华powerpms-reg.ashx-sql注入漏洞
---

# 普华Powerpms Reg.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/29 08:30
- 920浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

数据库

授权

SQL注入防护

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统Reg.ashx接口存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

看下Reg.ashx的实现逻辑

```
if (context.Request["hum"] != null && context.Request["hum"].ToString().Length > 0)
{
    string HumId = context.Request["hum"];
    Power.Systems.StdSystem.HumanBO bo = Power.Systems.StdSystem.HumanBO.FindByKey(HumId);
    if (bo != null)
```

当 **hum** 参数不为空且长度大于0时，进入Power.Systems.StdSystem.HumanBO使用FindByKey来查找，这个属于老熟人了。使用FindByKey查找，无过滤或校验，因此造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，就是朴实无华。

代码安全审计

# 漏洞复现

> weixin3.0/Reg.ashx
>
> 深入探索
>
> 编程语言教程
>
> 编码转换工具
>
> Nessus
>
> weixin3.0/static/Reg.ashx
>
> PowerMobile2/Reg.ashx
>
> 逻辑一样

```
POST /weixin3.0/Reg.ashx HTTP/1.1
Host: powerpms.mrxn.net
Content-Type: application/x-www-form-urlencoded

hum=SQLI_POC
```

[![普华Powerpms Reg.ashx SQL注入漏洞](images/img-001-6fb5ce9990f6.webp)](https://image.mrxn.net/fffe07381a914af8a3ef32786d27a52e.webp)

通过[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)成功在响应回显数据库版本信息

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
