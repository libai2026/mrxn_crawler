---
title: "用友NC content、portalpage 多个XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-portalpage-content-XXE.html
asset_dir: assets/用友nc-content、portalpage-多个xml实体注入（xxe）漏洞
---

# 用友NC content、portalpage 多个XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/27 09:47
- 796浏览
- [0评论](#comment)
- 1小时阅读

深入探索

sql

parse

语法分析

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可通过构造恶意XML内容，利用portalpage/doNew接口解析，实现任意文件读取或SSRF攻击等攻击，进而可能导致敏感信息泄露或进一步的系统入侵。

代码安全审计

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

根据官方漏洞通告部分可知漏洞点为 **PmlUtil**

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-001-61b4b0c46b74.webp)](https://image.mrxn.net/f4058a77c2da45978bb231dda4c4348a.webp)

那就搜索**PmlUtil**，找到了 `nc/uap/portal/util/PmlUtil.java` 看下它的实现吧

漏洞预警服务

```
public class PmlUtil {
    public static Digester getPortletDigester() {
        Digester pmlDigester = LfwXmlUtil.getDigester((String)Page.class.getName());
        if (pmlDigester == null) {
            pmlDigester = new Digester();
            LfwXmlUtil.setDigester((String)Page.class.getName(), (Digester)pmlDigester);
            PmlUtil.initPsmlDigester(pmlDigester);
        }
        return pmlDigester;
    }

    private static void initPsmlDigester(Digester pmlDigester) {
        pmlDigester.setValidating(false);
        pmlDigester.addObjectCreate("page", Page.class.getName());
        pmlDigester.addSetProperties("page");
        pmlDigester.addCallMethod("page/title", "setTitle", 0);
        String layoutClazz = Layout.class.getName();
        String portletClazz = Portlet.class.getName();
        pmlDigester.addObjectCreate("page/layout", layoutClazz);
        pmlDigester.addSetProperties("page/layout");
        pmlDigester.addSetNext("page/layout", "setLayout", layoutClazz);
        String layoutPath = "page/layout";
        for (int i = 0; i < 10; ++i) {
            String _layoutPath = layoutPath + "/layout";
            pmlDigester.addObjectCreate(_layoutPath, layoutClazz);
            pmlDigester.addSetProperties(_layoutPath);
            pmlDigester.addSetNext(_layoutPath, "addChild", layoutClazz);
            String portletPath = layoutPath + "/portlet";
            pmlDigester.addObjectCreate(portletPath, portletClazz);
            pmlDigester.addSetProperties(portletPath);
            pmlDigester.addSetNext(portletPath, "addChild", portletClazz);
            layoutPath = _layoutPath;
        }
    }
    //xml文件解析
    public static Page parser(File pml) throws PortalServiceException {
    Digester digester = PmlUtil.getPortletDigester();
    try {
        Page page = null;
        Digester digester2 = digester;
        synchronized (digester2) {
            page = (Page)digester.parse(pml);
        }
        String pmlName = pml.getName();
        page.setPagename(pmlName.substring(0, pmlName.length() - 4));
        return page;
    }
    catch (Exception e) {
        throw new PortalServiceException(e.getMessage(), e.getCause());
    }
}
//xml内容解析
public static Page parser(String pml) throws SAXException {
    Object object;
    Digester digester = PmlUtil.getPortletDigester();
    StringReader reader = null;
    try {
        Page page = null;
        reader = new StringReader(pml);
        object = digester;
        synchronized (object) {
            page = (Page)digester.parse((Reader)reader);
        }
        object = page;
    }
    catch (Exception e) {
        try {
            PortalLogger.error((String)LfwResBundle.getInstance().getStrByID("pserver", "PmlUtil-000002"), (Throwable)e);
            throw new SAXException(e.getMessage());
        }
        catch (Throwable throwable) {
            IOUtils.closeQuietly(reader);
            throw throwable;
        }
    }
    IOUtils.closeQuietly((Reader)reader);
    return object;
}
//文件流的形式解析
public static Page parser(InputStream in) throws SAXException {
    if (in == null) {
        return null;
    }
    Digester digester = PmlUtil.getPortletDigester();
    try {
        Page page = null;
        Object object = digester;
        synchronized (object) {
            page = (Page)digester.parse(in);
        }
        object = page;
        return object;
    }
    catch (Exception e) {
        PortalLogger.error((String)LfwResBundle.getInstance().getStrByID("pserver", "PmlUtil-000002"), (Throwable)e);
        throw new SAXException(e.getMessage());
    }
    finally {
        IOUtils.closeQuietly((InputStream)in);
    }
}
```

代码不多，很简单，就是对多个形式如string、流、文件几种形式的内容进行解析，且`PmlUtil.initPsmlDigester()` 方法中并未发现**禁用外部实体解析功能设置。**这意味着攻击者可以通过注入恶意 XML 实体来读取服务器本地文件、发起 SSRF 攻击或导致拒绝服务。

计算机科学

那就看下有那些地方调用了`PmlUtil.parser()` 方法，

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-002-796dca6d9338.webp)](https://image.mrxn.net/34de27cb0ff84d1fbabb97de04a5fad4.webp)

总共找到了4个地方的11个调用，只需关注首尾两个action相关的，中间的两个是不对外的。

在`PagePreviewAction.java` 中找到了**content**方法相关实现

## content

```
@Servlet(path="/page/preview")
public class PagePreviewAction
extends BaseAction {
    @Action
    public void content() {
        try {
            String page_xml = this.request.getParameter("page_xml");
            byte[] bytes = page_xml.getBytes("ISO-8859-1");
            String xml = new String(bytes, "UTF-8");
            xml = URLDecoder.decode(xml, "UTF-8");
            Page page = PmlUtil.parser((String)xml);
```

参数`page_xml`的值赋值给**page\_xml**后按照 `ISO-8859-1` 编码方式转换成字节数组，然后使用 `UTF-8` 编码方式，将上一步得到的字节数组 `bytes` 解码成一个新的 `String` 对象 `xml`，最后进行URL解码后就带入`PmlUtil.parser` 方法中进行解析，因此造成了XML实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。。

搜索引擎

再看其他几处

## portalpage

### doNew

```
@Servlet(path="/portalpage")
public class PortalPageManagerAction
extends BaseAction {
    private static MultipartResolver multipartResolver = new CommonsMultipartResolver();

    @Action(method="POST")
    public void doNew(@Param(name="groupid") String pk_group, @Param(name="pml") String pml) {
        LfwSessionBean ses = LfwRuntimeEnvironment.getLfwSessionBean();
        if (pml == null || ses == null) {
            return;
        }
        try {
            Page page = PmlUtil.parser((String)URLDecoder.decode(pml, "UTF-8"));
```

该方法还存在SQL注入漏洞，可参考 [用友NC portalpage/doNew sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-portalpage-doNew-groupid-sqli.html) （需要合法session）

代码安全审计

### doEdit

```
@Action(method="POST")
public void doEdit(@Param(name="pk") String pk, @Param(name="pml") String pml) {
    LfwSessionBean ses = LfwRuntimeEnvironment.getLfwSessionBean();
    if (pml == null || pk == null || ses == null) {
        return;
    }
    try {
        boolean pageNameHasModify;
        PtPageVO oldVersion = PortalServiceUtil.getPageQryService().getPageByPk(pk);
        if (oldVersion == null) {
            this.print("<result><success>false</success><detail>" + NCLangRes4VoTransl.getNCLangRes().getStrByID("pmng", "PortalPageManagerAction-000006") + "</detail></result>");
            return;
        }
        String pk_group = oldVersion.getPk_group();
        Page page = PmlUtil.parser((String)URLDecoder.decode(pml, "UTF-8"));
```

### importPml

> 文件上传形式
>
> 计算机科学

```
@Action
public void importPml() throws IOException {
    MultipartHttpServletRequest req = PortalPageManagerAction.getMultipartResolver(this.request);
    Map fileMap = req.getFileMap();
    ArrayList files = new ArrayList();
    String billitem = req.getParameter("billitem");
    if ("null".equals(billitem)) {
        billitem = "";
    }
    if (MapUtils.isNotEmpty((Map)fileMap)) {
        files.addAll(fileMap.values());
    }
    String name = ((MultipartFile)files.get(0)).getOriginalFilename();
    name = name.replace(".pml", "");
    InputStream in = ((MultipartFile)files.get(0)).getInputStream();
    try {
        Page page = PmlUtil.parser((String)IOUtils.toString((InputStream)in, (String)"UTF-8"));
```

该方法还存在SQL注入漏洞，可参考 [用友NC portalpage/importPml sql注入漏洞](https://mrxn.net/jswz/yonyou-nc-portalpage-importPml-billitem-sqli.html)

# 漏洞复现

## content

> 需要URL双重编码
>
> 漏洞预警服务

```
POST /portal/pt/page/preview/content?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

page_xml=XXE_POC
```

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-003-170aa3320b0f.webp)](https://image.mrxn.net/9b25a12720104df280bd2cd59e4333c6.webp)

成功在DNSLOG平台收到其DNS请求和HTTP请求

SQL注入检测工具

## importPml

```
POST /portal/pt/portalpage/importPml?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarybXJ4bi5uZXQ

------WebKitFormBoundarybXJ4bi5uZXQ
Content-Disposition: form-data; name="file"; filename="1.png"

XXE_POC
------WebKitFormBoundarybXJ4bi5uZXQ--
```

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-004-5818ea781827.webp)](https://image.mrxn.net/4917ffd246194c7b94a93fa7341d76b6.webp)

[![用友NC content、portalpage 多个XML实体注入（XXE）漏洞](images/img-005-227c45c7afcc.webp)](https://image.mrxn.net/eb712599d6bb4cb08094797a81773b4f.webp)

也是可以在DNSLOG平台收到DNS和HTTP请求

代码安全审计

# 参考

- [关于NC系统content接口的XML注入漏洞的安全通告](https://security.yonyou.com/#/noticeInfo?id=733)

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
- [4.1.content](#toc-4-1-)
- [4.2.portalpage](#toc-4-2-)
- [4.2.1.doNew](#toc-4-2-1-)
- [4.2.2.doEdit](#toc-4-2-2-)
- [4.2.3.importPml](#toc-4-2-3-)
- [5.漏洞复现](#toc-5-)
- [5.1.content](#toc-5-1-)
- [5.2.importPml](#toc-5-2-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
