---
title: "用友NC cartabletimeline/doList SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-cartabletimeline-doList-sqli.html
asset_dir: assets/用友nc-cartabletimelinedolist-sql注入漏洞
---

# 用友NC cartabletimeline/doList SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/3 09:02
- 702浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

云安全解决方案

漏洞扫描器

文件大小转换

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统的 cartabletimeline/doList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意的 SQL 语句注入请求参数，绕过身份验证或获取数据库敏感信息，进而可能导致任意数据读取、篡改甚至系统权限提升，影响系统的安全性和数据完整性。

SQL注入防护

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

漏洞预警服务

Nessus

文本剥离工具

直接看`VsmAction` 类的`doList`方法的实现逻辑吧

```
@Servlet(
    path = "/cartabletimeline"
)
public class VsmAction extends BaseAction {
    @Action
    public void doList() {
        HttpServletRequest request = this.request;
        String pks = request.getParameter("mtr");
        StringBuilder sd = new StringBuilder();
        sd.append("<?xml version='1.0' encoding='UTF-8' ?>");
        ICarTalbeService carTalbeService = (ICarTalbeService)NCLocator.getInstance().lookup(ICarTalbeService.class);
        StringBuffer sb = new StringBuffer();
        sb.append("(").append(pks).append(")");
        ApplyVO[] applyVOs = null;
        PersonVO[] personVOS = null;
        Map<String, PersonVO> personMap = new HashMap();

        try {
            applyVOs = carTalbeService.getVehicleApplyInfo((String)null, sb.toString(), (PaginationInfo)null);
            sd.append("<data>");
```

深入探索

SQL注入检测工具

授权

网络安全会议

跟进`ICarTalbeService`的`getVehicleApplyInfo`方法

```
public ApplyVO[] getgetUserVehicleApplyInfo(String pkUser, String whereSql, PaginationInfo pageInfo) throws LfwBusinessException {
    ApplyVO applyVOs = new ApplyVO();
    StringBuilder sb = new StringBuilder();
    if (!StringUtils.isBlank(whereSql)) {
        sb.append(" ( billstatus = 5 or billstatus = 6 ) and dispatchvehicle in  ").append(whereSql);
    }

    return (ApplyVO[])CRUDHelper.getCRUDService().queryVOs(applyVOs, pageInfo, sb.toString(), (Map)null, (String)null);
}
```

参数**mtr**这里被拼接进SQL语句中，整个过程没有对参数**mtr**进行校验或过滤，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华的！

代码安全审计

# 漏洞复现

> 需注意NC 大多数为Oracle 少数MSSQL

```
POST /portal/pt/cartabletimeline/doList HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

pageId=login&meapk=SQLI_POC
```

[![用友NC cartabletimeline/doList SQL注入漏洞](images/img-001-22adcf601f59.webp)](https://image.mrxn.net/2e7bb6fe2cce4b2ca98e44430c3e87e4.webp)

成功延时 3 秒

漏洞修复方案

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
