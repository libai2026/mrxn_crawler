---
title: "JeeWMS druid 未授权访问漏洞"
source: https://mrxn.net/jswz/JeeWMS-druid-unauth-accept.html
asset_dir: assets/jeewms-druid-未授权访问漏洞
---

# JeeWMS druid 未授权访问漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/4/24 08:32
- 1226浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

代码安全审计

企业安全咨询

恶意软件分析工具

---

# 漏洞简介

JeeWMS 是基于Java全栈技术打造的智能仓储中枢系统，具备多形态仓储场景深度适配能力（兼容3PL第三方物流与厂内物流双模式）。JeeWMS 存在 druid [未授权访问](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83 "未授权访问")，未授权攻击者可利用此漏洞获取系统如sql语句、url链接、Session等敏感信息。

网络安全

# 影响版本

最新版

# fofa语法

> `body="plug-in/lhgDialog/lhgdialog.min.js?skin=metro" || fid="cC2r/XQpJXcYiYFHOc77bg=="`

# 漏洞分析

深入探索

编码转换工具

网络安全课程

服务器安全服务

web.xml 里有关 druid 的过滤设置如下

```
<filter>
        <filter-name>druidWebStatFilter</filter-name>
        <filter-class>com.alibaba.druid.support.http.WebStatFilter</filter-class>
        <init-param>
            <param-name>exclusions</param-name>
            <param-value>/css/*,/context/*,/plug-in/*,*.js,*.css,*/druid*,/attached/*,*.jsp</param-value>
        </init-param>
        <init-param>
            <param-name>principalSessionName</param-name>
            <param-value>sessionInfo</param-value>
        </init-param>
        <init-param>
            <param-name>sessionStatEnable</param-name>
            <param-value>false</param-value>
        </init-param>
        <init-param>
            <param-name>profileEnable</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>
```

深入探索

安全工具开发

在线安全工具

防火墙软件

`exclusions`参数中配置了`*/druid*`，该模式使用Ant风格路径匹配规则，会匹配所有包含`/druid`的路径（例如`/druid/*`、`/api/druid/status`等）。若Druid控制台的访问路径（如`/druid/*`）未被其他安全机制（如认证、授权）保护，攻击者可直接访问Druid监控界面，造成 druid 未授权访问漏洞。

漏洞预警服务

再根据 druid 的servlet

```
<!-- druid -->
    <servlet>
        <servlet-name>druidStatView</servlet-name>
        <servlet-class>com.alibaba.druid.support.http.StatViewServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>druidStatView</servlet-name>
        <url-pattern>/webpage/system/druid/*</url-pattern>
    </servlet-mapping>
```

深入探索

数据库

物流软件安全

安全认证考试

得到具体的访问路径 `/webpage/system/druid/*`

# 漏洞复现

注意路径可能有或者没有 jeewms

文件大小转换

> /jeewms/webpage/system/druid/sql.html

```
GET /webpage/system/druid/websession.html HTTP/1.1
Host: localhost
```

[![JeeWMS druid 未授权访问漏洞](images/img-001-c9468e85a198.webp)](https://image.mrxn.net/c6cda1389d984a06aac215ed045351ef.webp)

也是可以成功未授权访问到session，可利用这些session进入后台

网络安全

或者查看sql语句等

[![JeeWMS druid 未授权访问漏洞](images/img-002-de97ace8312d.webp)](https://image.mrxn.net/3c4f9afd300a499dbf42d0b218632cd9.webp)

# 参考

- `https://gitee.com/erzhongxmu/JEEWMS/blob/master/src/main/webapp/WEB-INF/web.xml`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,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)

手机扫码阅读

文件大小转换
