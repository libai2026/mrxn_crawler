---
title: "索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞"
source: https://mrxn.net/jswz/sobey-Jzt-statistics-countJztArticleGroupByChannel2-sqli.html
asset_dir: assets/索贝融媒体-sobey-mcheditormchjztstatisticscountjztarticlegroupbychannel2-sql注入漏洞
---

# 索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/15 08:17
- 632浏览
- [0评论](#comment)
- 1小时阅读

深入探索

安全运维咨询

Web安全课程

安全

---

# 漏洞简介

索贝产品中的 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者可以通过构造恶意的SQL语句，获取数据库中的敏感信息，甚至可能导致数据库被完全控制。

SQL注入检测工具

# 影响版本

# fofa语法

> icon\_hash="689611853"||app="SOBEY-融媒体" || body="You need to enable JavaScript to run this app" && header="Sobey"

# 漏洞分析

深入探索

Web安全书籍

网络安全会议

安全研究工具

根据漏洞信息看下`mch/Jzt/statistics/countJztArticleGroupByChannel2`的实现逻辑

```
@RequestMapping(
    value = {"countJztArticleGroupByChannel2"},
    method = {RequestMethod.GET}
)
public Response countArticleGroupByChannel2(@RequestParam("token") String token, @RequestParam("siteCode") String siteCode, @RequestParam(value = "startTime",required = false) Long startTime, @RequestParam(value = "endTime",required = false) Long endTime, @RequestParam(value = "channelId",required = false) String channelId, @RequestParam(value = "ID",required = false) String ID) {
    List args = new ArrayList();
    StringBuffer sqlBuffer = new StringBuffer("select a.num,a.channelName,a.cname from ");
    sqlBuffer.append(" (SELECT SUM(h.num) as num,h.channelName as channelName,'合计' as cname from  ");
    sqlBuffer.append(" (SELECT count(DISTINCT id) AS num,channelName,cname FROM(");
    sqlBuffer.append(" select zcnarticle.id ");
    sqlBuffer.append(" , (SELECT zcchannel.channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" WHERE zccatalog.ID = zcnarticle.catalogID ) AS channelName ");
    sqlBuffer.append(" ,(SELECT zccatalog.Name FROM zccatalog INNER JOIN zcchannel ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID ) AS cname  ");
    sqlBuffer.append("  from zcnarticle  ");
    sqlBuffer.append(" , (SELECT DISTINCT zcnarticle.id articleid FROM zcnarticle where 1=1 ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" UNION SELECT zcnwxarticlerela.articleid FROM zcnwxarticle INNER JOIN zcnwxarticlerela ON zcnwxarticlerela.wxarticleId = zcnwxarticle.id ");
    sqlBuffer.append("  where 1=1 ");
    sqlBuffer.append(" and zcnwxarticle.ifval = '1' ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnwxarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnwxarticle.publishDate");
    sqlBuffer.append(" ) zcnarticleids ");
    sqlBuffer.append(" where zcnarticleids.articleid =zcnarticle.id ");
    sqlBuffer.append(" and zcnarticle.ifval = '1' ");
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" AND EXISTS ( SELECT channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID LIMIT 1)");
    if (channelId != null && ID == null) {
        sqlBuffer.append("and  catalogID in  (select distinct ID from  zccatalog where  1 = 1 ");
        sqlBuffer.append(String.format(" and prop3  in (%s) ", channelId));
        sqlBuffer.append(" ) ");
    }

    if (ID != null) {
        sqlBuffer.append(String.format(" and  catalogID  in (%s) ", ID));
    }

    sqlBuffer.append(")tmp  where  1= 1 ");
    sqlBuffer.append("  group by cname) h GROUP BY channelName UNION ");
    sqlBuffer.append("(SELECT count(DISTINCT id) AS num,channelName,cname FROM(");
    sqlBuffer.append(" select zcnarticle.id ");
    sqlBuffer.append(" , (SELECT zcchannel.channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID ");
    sqlBuffer.append(" WHERE zccatalog.ID = zcnarticle.catalogID ) AS channelName ");
    sqlBuffer.append(" ,(SELECT zccatalog.Name FROM zccatalog INNER JOIN zcchannel ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID ) AS cname  ");
    sqlBuffer.append("  from zcnarticle  ");
    sqlBuffer.append(" , (SELECT DISTINCT zcnarticle.id articleid FROM zcnarticle where 1=1 ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" UNION SELECT zcnwxarticlerela.articleid FROM zcnwxarticle INNER JOIN zcnwxarticlerela ON zcnwxarticlerela.wxarticleId = zcnwxarticle.id ");
    sqlBuffer.append("  where 1=1 ");
    sqlBuffer.append(" and zcnwxarticle.ifval = '1' ");
    SchemaSQLUtil.appendInCondition(sqlBuffer, "zcnwxarticle.status", ARTICLE_PUBLISH_STATUS_LIST);
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnwxarticle.publishDate");
    sqlBuffer.append(" ) zcnarticleids ");
    sqlBuffer.append(" where zcnarticleids.articleid =zcnarticle.id ");
    sqlBuffer.append(" and zcnarticle.ifval = '1' ");
    SchemaSQLUtil.appendTimeConditionSQL(startTime, endTime, sqlBuffer, args, "zcnarticle.publishDate");
    sqlBuffer.append(" AND EXISTS ( SELECT channelname FROM zcchannel INNER JOIN zccatalog ON zccatalog.prop3 = zcchannel.ChannelID WHERE zccatalog.ID = zcnarticle.catalogID LIMIT 1)");
    if (channelId != null && ID == null) {
        sqlBuffer.append("and  catalogID in  (select distinct ID from  zccatalog where  1 = 1 ");
        sqlBuffer.append(String.format(" and prop3  in (%s) ", channelId));
        sqlBuffer.append(" ) ");
    }

    if (ID != null) {
        sqlBuffer.append(String.format(" and  catalogID  in (%s) ", ID));
    }

    sqlBuffer.append(")tmp  where  1= 1 ");
    sqlBuffer.append("GROUP BY cname))as a ORDER BY a.channelName,a.cname DESC");
    QueryBuilder queryBuilder = new QueryBuilder("" + sqlBuffer, args.toArray());
    List<Map<String, Object>> data = queryBuilder.executeListMap();
    return Response.success(data);
}
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞](images/img-001-acf3ef0c1cef.webp)](https://image.mrxn.net/af9a1f2fe37e4c8aa2d15f998437a143.webp)

代码一看就很明了了，**channelId**和**ID**无任何过滤或校验，被直接拼接在in子语句中，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

如果没有String.format，就不存在，因为默认的append方法底层是参数化查询。

代码安全审计

# 漏洞复现

```
GET /sobey-mchEditor/js/..;/mch/Jzt/statistics/countJztArticleGroupByChannel2?siteCode=&token=&userCode=admin&channelId=1&catalogid=1&channelId=SQLI_POC HTTP/1.1
Host: sobey.mrxn.net
```

[![索贝融媒体 /sobey-mchEditor/mch/Jzt/statistics/countJztArticleGroupByChannel2 SQL注入漏洞](images/img-002-6ade200469c3.webp)](https://image.mrxn.net/5e02fa3ac6f24f31ba827d2d464165e8.webp)

成功利用报错注入在响应回显当前数据用户

漏洞修复方案

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

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAANtUlEQVR4Aeyb4Xbjxg6D9+v7v3NrDAKbpEeKm91N/EM9QUCCIDUryrGTc+8/v379+vf/4t/yX3ojJf8dnrOST841pNd4l0sTpk+aIF0sKBYU76BaxSue6j+LtZBft4Ev4Tbo6Su9wC/gXo8eTiH5GQNrVjzgHMyZdcbpPfPMGuzng3Uwz9lgfc5THu9nLK+wFqLgwnvcgbYQ8Kah89lRwd548iQkD08del984njBnuSqCbDXaw3sAbNqO4DruYZ455OmmqBYUCwo/gzg60Dn2dcWMotX/v134I8vBM6fgPlPhO4HpmW9nwD397lpgOeanlxheqUJwJqbOpDwzsDyyC+kANbBrJoAxPJl/uML+fJJrsZ1B35rIfB4IvSECGtq+Qasp6xIK5RXWMn4Bu5RXUgZrO9y6LV41C8kD0urkA77GWAdzOlTT4X0mn8l/q2FfOWCV8/5HWgL0YZ3OBpRvfFUrcbgpws6y5PeI5ZHmHVpE/FAvw7s8/j/Ns9zJp/XbQuZxS/nV+OX78BaCOyfHuj6vApwl4D2XgE9j/HoyVD9qAaedVZXf8X0HuXwmJ3+I2/qRww8lYB1X+Cc07gWkuTin78D/+Rp+D9cjw3efDToefTM3+WpQe+Fnqd3svqnBq/3pl8szFkzhz4bnNdexV/B9QqZd/uH87YQ8KbBPM8G1sFc6/NpSA3sBfPUlUOvSavI7KopBvfBg6UL6QlLqwD3VO0ohu6dM5ODffDgzARryY/4H+Bey+AIwHpDSj7rycXxwHkP9Lr61C8oFhQLiiug98ojyCMWFAvQveBcngp5BXAdHlx9iuUTwB7FFfJMQPfCPgfr7RVSh1/xz9yB9aYO3g6Yc5RsOzn0OpDSeiXB8x/5gFW7G0cADOWRzus/Ko6ANVs+eMTK7fi16sCv+R9wrwGrrL6KJd6+Act7C9dXPCu5fYNev0nLDyhcSE8YWJ5VvH2Lfr1Cbjfjnb7aQrKleUDwNlOvHG+0o/wzXfXMAF9PWsHhn9+rB9ybWaklh16PLh+4plgA59UjPTjSUxcfeY70thANuPCzd2B9yprbOsrBT0yODCR8YmD9jMyscIzJxdHC0gTwjOiT5RHg+b1resGz5BfAOZilzZ6jHNxzVJeueQLYC2bVBHAujwDOr1eI7s4bYX3KynnAW4I9a5MCuF7jOUM1YerJzxg8f3pgr9frzJ7k8gjgGYqF1OHxKgN7UpusPiG6YgGI9MSqC8D6yfFk+BCuV8jHjXgXWu8hOYw2WBE9DN5uPNJrrDwAe5OfMey9R7MzC577jnrA3tTBeWaJ4Vmr+uyF7lcdrIFZmqA5FdKEqim+XiG6C2+EtRDwNnMu6Hl0bVRILgZ7way6oFqFNKFqiuHxs1v5VwDc24D1MxrMumYFdP3eeAviu4XbLzjuTUNmhME9qU+GXl8LmaYr/7k70D5lzWNky2HwNsEsf2qKBXBt6qrtIB+4Z1eXBr2uHkG1I6guzLo0AT5mfhikfYSHJI8Avfew4VaQX7iF60uxAPsZ1ytk3ab3+bYWoo0JOZZiITl4m9KE6GI4rqkegH1HuXSwR9cQwLlqO8gjqAb2KhfAOexZPRXw8Kl/B7AnffHAQwfHYI4Xeh49M8LrYy90M/Q8ZrCePEPFsK+BdXkEeM4zLwz2JFefMHPoPtXlO4M8FWde8Px40pd8x0ee6NBnzhnrFTLFK/+5O7AWcrQ96NuML8eF54+s0HviTW84uhj2PaoJu56qA0oXgPWxNz3hVbx9A9fBnHrlm237Be6ZxfRKB3uqVnXFFWA/mNdCquGKf/YOtI+92epk8Pags44O1hRXgPXMSg26rnpqYWlC8jC4d+byQq/FE5ZHOMqjV5ZfgP1ssA7m2gvWwKw5FfFGS369QnIn3oTXQsBbzJnAOZizxcnxi89qqgfxJRdHA19PmgDOwSytovZVXTHse1QToNfBOaByQ64TbsWRxBMe5fX+Bo9rAEuLfy1kNl35b9+BLw9Yv4ekG7yt5Nlacuh16fGAa2BWrQK6Ds6Bu23OSiF68jCwni7l0zNzeYToYWlBNPBcMKf+GYP98ODPelIH91yvkNyRN+H2KStnmk/K1JPvOL3heGZedfDTES2cHnA9+axLjxYG94A5+hHXGYqFI++Zrr6KeMHnqLVdfL1CcsfehNdC5qbA28wZwTl0Vh2sKa4A67DneOH5t/3Uwjkf7GfBQ589szd1ePSA41lLb/Rw9HB0MXgWmKVVgHUwpwbO10IiXvzzd2AtBLwdMM/NJ5+s40dTXBF9cjxVB1931sA6mFMP1xmJU5ucOvRZ0eWHXgPnYJbnM2Te5PRFTz55LWSKV/5zd2At5LOt5Xjw+pMye6D3gnN4vIeAtfTmXJNTDwMJP+XMOjNOz8zTC6zfg3Z1cC3eybseedovhhIE2A87GqKeAPa9qYd3s6LBazPqrMRh8AzY87xWcnFmhOF8RnyVNUeo2i4Gz05tvUKSTL7y778DayHgLWmjFTkOuA6dVQdrioX0K66YOrhPOjgGc/rgtRzsA9J6Z83f4W44CdIXy8yB9SMLzPKBY+ismgBdz8zwWoiMF97jDmz/dALeYraWoyavPGvJwTNmXnsVqy6ukFYBfVb1zrj2KQb3QmfVKoB7Cqwn/y58BLDXP8rr/+GVeHLOOfWZX6+QeUd+OF+fsrI96E8AOD+q6+ypKX4F4JnxgnN4cGaG4/0TnJng69WZYG16ksf7WS7f9ECfPevqEa5XiO7CG6EtZG7ts1z/DvDmFQvQ86MZYF/qlTVnh3jAvdUDz1qtpzda8rD0Gis/AvRrwSPPDLCWPAzWwZxrgPO2kBQv/rk7sBYC3g6Yj7YJroN5d+z0huNJDr0XiOXOQPuUc9YL3Zsh6UkO9oF56slf4Tk7PeDZQKQ7A+vfdNQb41pIku/h6ypnd6D9HnK0vejhDITjPwxWD/jpgIc/s8TxHjG4X96K6q+64tQU75B6ZfB1wJw+6HntURyfWLmgWAD3ShOg59IqrldIvRtvEK+FaJMCeHtgnueDvT59yqF7NV+Arst7BNh7Ya9rDrgGnVWrANd1ponq28Xg3tTAORDpkOe1gPbeshZy2H0Vvv0OrN/UP7sq9C1WP+xrR09CesF9yuERK0+v4h1SD1dPtMnga4A5dXCuGeB4V1M9SD155bNa9SWe/vYKmcXZBP3A8scDriUPg3V5K1LfMbzWAw8fON7Nk1avrRi6H5BtAVg/RlZy+ya/cAvbl7SKVhxJfJGhXwOct4XEfPHP3YG2EPCWcpy51ZnD42NseqDPiD45s+B5xvQmB88Gc2aonhhcA7NqO8S/4+kHzwLzrCfXrMRhaULyydBntoVM85V//x1YvxhC39LRMcA+MGvz8IiVB5mRHOwDc+pisAbm2SNPRepVS3xWi2fHwF2eM2YOrPcYMN8bbwFYA/NNal+w12O6XiG5E2/C7WNvnoRwzgjeavQwPH7+gz2zJ3l6wtHFO+1Mh34teY8A9oJ5+sC6zpAaWDvK5a2A7ldf6uAamFUTUp98vUJ0d94I6z0kW5rngr5VcA7m6T/LYd+ja0OvQc8zV14hOdgHRLqzfBUpAIc//+NJ38yjQ59R9cTpDUcPR598vULmHfnhfC0E+sbBebZ5xtC9898D53X553xpArhXsQA9T59qAdgDnVPf9aQ2OV7wrP9br37wDOhcPYrXQhRceI87sP2UlaNB3yb0XL48RYoFsGfqqgnguuIAupbeMOzr6ZevxsqD6JNTD4OvAdytwHq/mZ674SNI/SNtlFo4xZlHv14huRNvwutTVs4C/YnIFidPPxBp/c8p5QfW03UvfASqCfBcB2tg/mi5z0wOroNZOjiGzqoJuqYAvQ7OVZNPgGj/rmtDz+WpgEcdHIM5PtjnYB3M1yskd+xNeC1ET0cFeFvzjNB19bzikQ967+yrufwC9B5pQvUqBkQN8lWkGG3m8PirQ2rAepWnB5zPes0Th6H3ZFbqM18LSTE8TVNPHUhpHRyO/1F340ewmxHtw7J+XEhLPlm1iXiA+5ngOU5f/DuenuTh9NQ88eR4J4PPFn27kBQv/v47sD72grcEr/HumHkiwDPiiZ4cXAez9COPahXw6Jl6zRVn5mTVdpAPPF+xsPNJA/sUHwHOPZovpF+xcL1CckfehNdCtJlXMM+snp0mPUj9szw+cbzgpwzMqu0g/9ThvCd+sA+IdGegvQ/dCx+BriuAfR/yIunCSk6+ySOAZ6yFnPiv0jffgbYQ8Jag89mZtF0hHnitF+xLnxisgVlzBdUExYJiAeyDB0vfAexRvwDOd95o8lVMHTwjHtXBGnRWTYCug3PVhLYQCRf+/h04u8JvLQS8XXhwnpbw2cWParM3Ofg6yV9h6D3gPNfOjOSVoXtrTfFZr+rCK57q+62FaNCFP3sH/thC8iSAnyow57jgPL7oyhNPBvdMfZeDvWCOR/MF6HrqYXkCsDd5PJPBvqrPHrAn+uT0gn1/bCEZfPHv3YG2kLm95EeXUP2spjp489OnmiAdugecqy7APlevAM9/Q5MugHsV7wCPOjxiecE5dFZN0NkExRPShamDZ01dXqEtZJqu/PvvwFoIeGtwzmfHA/fGAz2PHobzenxiPTkCvN6jPkF9O6h2hOmPLzr0c4Bz1eMFa8lf5bWQV82X7+/fgf8AAAD//z3cEZ8AAAAGSURBVAMAMufQzr0Jt8kAAAAASUVORK5CYII=)

手机扫码阅读
