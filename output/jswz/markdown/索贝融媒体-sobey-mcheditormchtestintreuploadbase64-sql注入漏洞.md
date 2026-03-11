---
title: "索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-TestInt-reUploadBase64-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchtestintreuploadbase64-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/22 08:27
- 732浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

防火墙软件

安全研究报告

Web安全书籍

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/TestInt/reUploadBase64 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/TestInt/reUploadBase64`的实现逻辑

```
@RequestMapping(
    value = {"/reUploadBase64"},
    method = {RequestMethod.GET}
)
public Response reUploadBase64(@RequestParam(value = "ids",required = false) String ids, String token) {
    QueryBuilder qb = new QueryBuilder("select id from zcnarticle where 1=1 ");
    if (!StringUtils.isEmpty(ids)) {
        SchemaSQLUtil.appendInCondition(qb, "id", Arrays.asList(ids.split(",")));
    } else {
        qb.append("  and content like '%base64,%' union  select id from zcnarticle where 1=1 and logo like '%base64,%' ");
    }

    List<Map<String, Object>> rows = qb.executeAliasListMap();
```

深入探索

服务器安全服务

Web安全课程

VPN服务

参数**ids**无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞；但是ids会被逗号分割，因此利用有限。

代码安全审计

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/TestInt/reUploadBase64?ids=SQLI_POC&siteCode=1&token=1 HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/TestInt/reUploadBase64 SQL注入漏洞](images/img-001-6b5f004d4a34.webp)](https://image.mrxn.net/2f02877a84934ca589104f2b0aa90a25.webp)

报错回显获取到当前表名前缀 articl\_c7ee17

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
