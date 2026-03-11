---
title: "万户OA jigeObj_iframe.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-gov_documentmanager-jigeObj_iframe-sqli.html
asset_dir: assets/万户oa-jigeobj_iframe.jsp-sql注入漏洞
---

# 万户OA jigeObj\_iframe.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/30 15:25
- 848浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

安全研究工具

恶意软件分析工具

编程语言教程

---

# 漏洞简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice) 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。万户 ezOFFICE jigeObj\_iframe.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql注入)漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/漏洞)获取数据库权限，深入利用可获取服务器权限。

SQL注入检测工具

# 影响版本

> 老旧版本

# fofa语法

> app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞分析

深入探索

安全研究报告

文件大小转换

数据库

直接看jigeObj\_iframe.jsp文件里的业务实现逻辑吧，非常简单明了

[![万户OA jigeObj_iframe.jsp SQL注入漏洞](images/img-001-25f0e00633f7.webp)](https://image.mrxn.net/8f1e8841286a46d180a9c271aceea8f3.webp)

```
String mRecordID=request.getParameter("RecordID");
String mTemplate=request.getParameter("Template");
//取得编号
if ( mRecordID==null||mRecordID.toString().equals("null")){
   mRecordID="";    //编号为空
}

//第一次， id 为空
if(mRecordID==null||mRecordID.equals("")||mRecordID.equals("null")){
isFirstIn="1";
}
//打开数据库
DBstep.iDBManager2000 DbaObj=new DBstep.iDBManager2000();
if ( DbaObj.OpenConnection())
{
  String mSql="Select * From Document Where RecordID='"+ mRecordID + "'";
  try
   {  
  if(!mRecordID.equals("")){
      result=DbaObj.ExecuteQuery(mSql);
```

参数`RecordID` 被直接拼接进SQL语句中然后用`ExecuteQuery`执行，所有参数都**没有过滤或校验**，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

权限绕过分析参考：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

代码安全审计

```
GET /defaultroot/modules/govoffice/gov_documentmanager/jigeObj_iframe.jsp;.js?RecordID=1'
Host: ezoffice.mrxn.net
```

其他万户OA 相关[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

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
