---
title: "用友NC mtapptimeline/doApply SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-mtapptimeline-doApply-sqli.html
asset_dir: assets/用友nc-mtapptimelinedoapply-sql注入漏洞
---

# 用友NC mtapptimeline/doApply SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/26 08:27
- 795浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

CRM

软件

身份验证

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统的 mtapptimeline/doApply 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

SQL注入检测工具

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"
>
> 代码安全审计

# 漏洞分析

直接看`MtAppTimeLineAction` 类的`doApply`方法的实现逻辑吧

```
@Action
public void doApply() {
    HttpServletRequest request = this.request;
    String maEventPk = request.getParameter("meapk");
    IMeetingApplyQueryService qs = (IMeetingApplyQueryService)NCLocator.getInstance().lookup(IMeetingApplyQueryService.class);
    String whereSQL = "pk_mtappdoc='" + maEventPk + "'";

    try {
        MeetingApplyEventVO[] maEvents = qs.queryMeetingApplyEvents(whereSQL, (SQLParameter)null);
        String pk_currentuser = LfwRuntimeEnvironment.getLfwSessionBean().getPk_user();
        StringBuilder sd = new StringBuilder();
        sd.append(this.bulidupXml(maEvents, pk_currentuser));
        ResponseUtils.outputClientStreamWithGzip(this.getResponse(), "text/xml", sd.toString());
    } catch (BusinessException e) {
        Logger.error(e.getMessage(), e);
        throw new LfwRuntimeException(e.getMessage());
    }
}
```

深入探索

网络安全培训

安全研究工具

文本剥离工具

参数**meapk**这里被拼接进SQL语句中，整个过程没有对参数**meapk**进行校验或过滤，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华的！

漏洞扫描服务

# 漏洞复现

> 需注意NC65 大多数为Oracle 少数MSSQL

```
POST /portal/pt/mtapptimeline/doApply HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

pageId=login&meapk=SQLI_POC
```

[![用友NC mtapptimeline/doApply SQL注入漏洞](images/img-001-738b2826aeec.webp)](https://image.mrxn.net/767207beed194f1e8e770dc3e40aa187.webp)

通过报错注入成功在响应回显当前数据库用户！

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
